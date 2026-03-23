import re
import pandas as pd
import ast

class UserManager:
    def __init__(self, data_manager):
        self.dm = data_manager
        self.current_user = None

    def safe_eval_list(self, value):
        if isinstance(value, str):
            try:
                return ast.literal_eval(value)
            except Exception:
                return []
        return value

    def register_user(self):
        username = input("Username: ")
        if "username" not in self.dm.user_df.columns:
            print(" Το user_df δεν περιέχει στήλη 'username'. Δημιουργείται νέα δομή.")
            self.dm.user_df = pd.DataFrame(columns=["id", "username", "password", "address", "city", "orders", "favorites", "balance"])

        if username in self.dm.user_df['username'].values:
            print("Username already exists.")
            return

        password = input("Password (>=8 chars, 1 special char): ")
        if not self.validate_password(password):
            print("Invalid password.")
            return

        address = input("Address: ")
        city = input("City: ")
        new_id = self.dm.user_df['id'].max() + 1 if not self.dm.user_df.empty else 1

        new_user = pd.DataFrame([{
            "id": new_id,
            "username": username,
            "password": password,
            "address": address,
            "city": city,
            "orders": "[]",
            "favorites": "[]",
            "balance": 100.0
        }])

        self.dm.user_df = pd.concat([self.dm.user_df, new_user], ignore_index=True)
        self.dm.save_data()
        print(" User registered successfully.")
    
    #Συνδεση στο account
    def login_user(self):
        for attempt in range(3):
            username = input("Username: ")
            password = input("Password: ")

            if "username" not in self.dm.user_df.columns:
                print(" Δεν υπάρχει η στήλη 'username' στο user_df.")
                return False

            user = self.dm.user_df[
                (self.dm.user_df['username'] == username) &
                (self.dm.user_df['password'] == password)
            ]
            if not user.empty:
                self.current_user = user.iloc[0].to_dict()
                print(f"Welcome, {username}!")
                return True
            print(" Incorrect credentials.")
        print(" Too many failed attempts.")
        return False

    #Πιστοποιηση Στοιχειων
    def validate_password(self, password):
        return len(password) >= 8 and re.search(r'\W', password)
    #Ελεγχος Υπολοιπου
    def check_balance(self):
        print(f" Current balance: {self.current_user['balance']} €")

    #Προσθηκη αγαπημενων σε ενα χρηστη
    def add_to_favorites(self, book_id):
        favorites = self.safe_eval_list(self.current_user["favorites"])
        if book_id not in favorites:
            favorites.append(book_id)
            self.current_user["favorites"] = str(favorites)
            idx = self.dm.user_df[self.dm.user_df["id"] == self.current_user["id"]].index[0]
            self.dm.user_df.at[idx, "favorites"] = str(favorites)
            self.dm.save_data()
            print(f" Book ID {book_id} added to favorites.")
        else:
            print("Book already in favorites.")

    #Αφαιρεση απο τα αγαπημενα
    def remove_from_favorites(self, book_id):
        favorites = self.safe_eval_list(self.current_user["favorites"])
        if book_id in favorites:
            favorites.remove(book_id)
            self.current_user["favorites"] = str(favorites)
            idx = self.dm.user_df[self.dm.user_df["id"] == self.current_user["id"]].index[0]
            self.dm.user_df.at[idx, "favorites"] = str(favorites)
            self.dm.save_data()
            print(f" Book ID {book_id} removed from favorites.")
        else:
            print("Book not found in favorites.")
    
    #Προβολη αγαπημενων 
    def show_favorites(self):
        favorite_ids = self.safe_eval_list(self.current_user["favorites"])
        print(" Favorite Books:")
        for book_id in favorite_ids:
            book = self.dm.books_df[self.dm.books_df["id"] == book_id]
            if not book.empty:
                print(f" - {book.iloc[0]['title']} by {book.iloc[0]['author']} (ID: {book_id})")
            else:
                print(f" - Book ID {book_id} not found.")
    
    #Ενημερωση στοιχειων προφιλ χρηστη
    def update_profile(self):
        print("🔧 Update Profile")
        address = input("New address (leave empty to keep current): ")
        city = input("New city (leave empty to keep current): ")
        password = input("New password (leave empty to keep current): ")

        idx = self.dm.user_df[self.dm.user_df["id"] == self.current_user["id"]].index[0]
        if address:
            self.dm.user_df.at[idx, "address"] = address
            self.current_user["address"] = address
        if city:
            self.dm.user_df.at[idx, "city"] = city
            self.current_user["city"] = city
        if password:
            if self.validate_password(password):
                self.dm.user_df.at[idx, "password"] = password
                self.current_user["password"] = password
            else:
                print(" Invalid password. It was not changed.")

        self.dm.save_data()
        print(" Profile updated successfully.")


    def show_favorites_availability_and_price(self):
        favorite_ids = self.safe_eval_list(self.current_user["favorites"])
        print("🔍 Favorite Books – Availability & Price:")
        for book_id in favorite_ids:
            book = self.dm.books_df[self.dm.books_df["id"] == book_id]
            if not book.empty:
                b = book.iloc[0]
                status = " Available" if b["availability"] else " Unavailable"
                total_price = b["cost"] + b["shipping_cost"]
                print(f" - {b['title']} ({status}) – Total: {total_price:.2f} €")
            else:
                print(f" - Book ID {book_id} not found.")

    #Αγορα βιβλιου
    def buy_book(self, book_id):
        book = self.dm.books_df[self.dm.books_df["id"] == book_id]
        if book.empty:
            print(" Book not found.")
            return

        book_data = book.iloc[0]
        if not book_data["availability"]:
            print(" Book not available.")
            return

        total_cost = book_data["cost"] + book_data["shipping_cost"]
        if self.current_user["balance"] < total_cost:
            print(" Not enough balance.")
            return

        orders = self.safe_eval_list(self.current_user["orders"])
        orders.append(book_id)
        self.current_user["orders"] = str(orders)
        self.current_user["balance"] -= total_cost

        idx = self.dm.user_df[self.dm.user_df["id"] == self.current_user["id"]].index[0]
        self.dm.user_df.at[idx, "orders"] = str(orders)
        self.dm.user_df.at[idx, "balance"] = self.current_user["balance"]
        self.dm.save_data()

        print(f" You bought '{book_data['title']}' for {total_cost:.2f} €")
    
    #Ακυρωση Παραγγελιας 
    def cancel_order(self, book_id):
        orders = self.safe_eval_list(self.current_user["orders"])
        if book_id not in orders:
            print(" Book not found in your orders.")
            return

        book = self.dm.books_df[self.dm.books_df["id"] == book_id]
        if book.empty:
            print(" Book data missing. Cannot refund.")
            return

        book_data = book.iloc[0]
        refund = book_data["cost"] + book_data["shipping_cost"]
        orders.remove(book_id)
        self.current_user["orders"] = str(orders)
        self.current_user["balance"] += refund

        idx = self.dm.user_df[self.dm.user_df["id"] == self.current_user["id"]].index[0]
        self.dm.user_df.at[idx, "orders"] = str(orders)
        self.dm.user_df.at[idx, "balance"] = self.current_user["balance"]
        self.dm.save_data()

        print(f"↩️ Order cancelled. {refund:.2f} € refunded to your balance.")
    
    #Προβολη παραγγελιων 
    def show_orders(self):
        order_ids = self.safe_eval_list(self.current_user["orders"])
        print(" Your Orders:")
        for book_id in order_ids:
            book = self.dm.books_df[self.dm.books_df["id"] == book_id]
            if not book.empty:
                print(f" - {book.iloc[0]['title']} by {book.iloc[0]['author']} (ID: {book_id})")
            else:
                print(f" - Book ID {book_id} not found.")

    #Βαθμολογια Βιβλιων
    def rate_book(self, book_id):
        orders = self.safe_eval_list(self.current_user["orders"])
        if book_id not in orders:
            print(" You can only rate books you've purchased.")
            return

        book = self.dm.books_df[self.dm.books_df["id"] == book_id]
        if book.empty:
            print(" Book not found.")
            return

        rating = int(input(" Give a rating (1-5): "))
        if rating < 1 or rating > 5:
            print(" Invalid rating.")
            return

        ratings = self.safe_eval_list(book.iloc[0]["ratings"])
        ratings.append(rating)

        idx = self.dm.books_df[self.dm.books_df["id"] == book_id].index[0]
        self.dm.books_df.at[idx, "ratings"] = str(ratings)
        self.dm.save_data()

        print(f" You rated '{book.iloc[0]['title']}' with {rating} stars.")

    #Προβολη βαθμολογιων
    def show_book_rating(self, book_id):
        book = self.dm.books_df[self.dm.books_df["id"] == book_id]
        if book.empty:
            print(" Book not found.")
            return

        ratings = self.safe_eval_list(book.iloc[0]["ratings"])
        if not ratings:
            print(f" No ratings yet for '{book.iloc[0]['title']}'.")
            return

        avg_rating = sum(ratings) / len(ratings)
        print(f" '{book.iloc[0]['title']}' - Average Rating: {avg_rating:.2f} ({len(ratings)} ratings)")

    #Προταση Βιβλιων
    def suggest_books(self):
        favorite_ids = self.safe_eval_list(self.current_user["favorites"])

        if not favorite_ids:
            print(" No favorites yet. Here are some random suggestions:")
            sample_books = self.dm.books_df.sample(n=min(5, len(self.dm.books_df)))
            for _, row in sample_books.iterrows():
                print(f" - {row['title']} ({row['categories']})")
            return

        category_count = {}
        for book_id in favorite_ids:
            book = self.dm.books_df[self.dm.books_df["id"] == book_id]
            if not book.empty:
                categories = book.iloc[0]["categories"]
                for cat in categories:
                    category_count[cat] = category_count.get(cat, 0) + 1

        if not category_count:
            print(" Could not determine categories from favorites.")
            return

        most_common_category = max(category_count, key=category_count.get)
        print(f" Suggesting books from category: {most_common_category}")

        favorite_ids_set = set(favorite_ids)
        orders_set = set(self.safe_eval_list(self.current_user["orders"]))

        suggestions = self.dm.books_df[
            self.dm.books_df["categories"].apply(lambda cats: most_common_category in cats) &
            (~self.dm.books_df["id"].isin(favorite_ids_set | orders_set))
        ]

        if suggestions.empty:
            print("No new suggestions found in this category.")
        else:
            sample_suggestions = suggestions.sample(n=min(5, len(suggestions)))
            for _, row in sample_suggestions.iterrows():
                print(f" - {row['title']} by {row['author']} (ID: {row['id']})")
