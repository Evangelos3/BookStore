import pandas as pd
import ast
import os
import matplotlib.pyplot as plt
import numpy as np


class AdminManager:
    def __init__(self, data_manager):
        self.dm = data_manager

    def admin_menu(self, admin_id):
        while True:
            print("\n Admin Menu:")
            print("1. Προσθήκη νέου βιβλίου")
            print("2. Διαγραφή βιβλίου")
            print("3. Ενημέρωση στοκ βιβλίου")
            print("4. Ενημέρωση στοιχείων βιβλίου")
            print("5. Προβολή όλων των βιβλίων")
            print("6. Προβολή στατιστικών αξιολόγησης βιβλίων")
            print("7. Διαγραφή αξολόγησης")
            print("8. Προσθηκη Νεων Βιβλιων")
            print("0. Έξοδος Admin Menu")
            option = input("Επιλογή: ")

            if option == "1":
                self.add_book()
            elif option == "2":
                book_id = int(input("Book ID προς διαγραφή: "))
                self.delete_book(book_id)
            elif option == "3":
                book_id = int(input("Book ID για ενημέρωση στοκ: "))
                new_copies = int(input("Νέο απόθεμα (copies): "))
                self.update_stock(book_id, new_copies)
            elif option == "4":
                book_id = int(input("Book ID για ενημέρωση στοιχείων: "))
                self.update_book_info(book_id)
            elif option == "5":
                self.show_all_books()
            elif option == "6":
                self.show_book_statistics()
            elif option == "7":
                book_id = int(input("Book ID για διαγραφή review: "))
                self.delete_review(book_id)
            elif option == "8":
                filename = input("Όνομα αρχείου CSV: ")
                self.import_books_from_csv(filename)
                
    
            elif option == "0":
                print("Έξοδος από Admin Menu.")
                break
            else:
                print("Μη έγκυρη επιλογή.")

        self.dm.save_data()
    
#Προσθηκη Βιβλιου
    def add_book(self):
        new_id = self.dm.books_df['id'].max() + 1 if not self.dm.books_df.empty else 1
        title = input("Τίτλος: ")
        author = input("Συγγραφέας: ")
        publisher = input("Εκδότης: ")
        categories = input("Κατηγορίες (χωρισμένες με ','): ").split(",")
        categories = [cat.strip() for cat in categories]
        cost = float(input("Κόστος: "))
        shipping_cost = float(input("Κόστος αποστολής: "))
        availability = input("Διαθέσιμο; (yes/no): ").lower() == "yes"
        copies = int(input("Αριθμός αντιτύπων: "))
        bookstores = []  # Προαιρετικά μπορούμε να βάλουμε bookstore ids

        new_book = pd.DataFrame([{
            "id": new_id,
            "title": title,
            "author": author,
            "publisher": publisher,
            "categories": categories,
            "cost": cost,
            "shipping_cost": shipping_cost,
            "availability": availability,
            "copies": copies,
            "bookstores": bookstores,
            "ratings": []
        }])

        self.dm.books_df = pd.concat([self.dm.books_df, new_book], ignore_index=True)
        self.dm.save_data()
        print(f" Προστέθηκε το βιβλίο '{title}'.")
    
    #Διαγραφη Βιβλιου
    def delete_book(self, book_id):
        book = self.dm.books_df[self.dm.books_df["id"] == book_id]
        if book.empty:
            print(" Book not found.")
            return
        self.dm.books_df = self.dm.books_df[self.dm.books_df["id"] != book_id]
        self.dm.save_data()
        print(f" Book ID {book_id} deleted.")

    #Ενημερωση του Στοκ
    def update_stock(self, book_id, new_copies):
        book = self.dm.books_df[self.dm.books_df["id"] == book_id]
        if book.empty:
            print(" Book not found.")
            return
        idx = self.dm.books_df[self.dm.books_df["id"] == book_id].index[0]
        self.dm.books_df.at[idx, "copies"] = new_copies
        self.dm.save_data()
        print(f"Updated stock of Book ID {book_id} to {new_copies} copies.")

    #Ενημερωση στοιχειων Βιβλιου
    def update_book_info(self, book_id):
        book = self.dm.books_df[self.dm.books_df["id"] == book_id]
        if book.empty:
            print(" Book not found.")
            return

        idx = self.dm.books_df[self.dm.books_df["id"] == book_id].index[0]

        cost = input("Νέο κόστος (enter για καμία αλλαγή): ")
        shipping_cost = input("Νέο κόστος αποστολής (enter για καμία αλλαγή): ")
        availability = input("Διαθέσιμο (yes/no ή enter για καμία αλλαγή): ")

        if cost:
            self.dm.books_df.at[idx, "cost"] = float(cost)
        if shipping_cost:
            self.dm.books_df.at[idx, "shipping_cost"] = float(shipping_cost)
        if availability.lower() in ["yes", "no"]:
            self.dm.books_df.at[idx, "availability"] = availability.lower() == "yes"

        self.dm.save_data()
        print(f" Book ID {book_id} updated.")

    #Προβολη ολων των βιβλιων
    def show_all_books(self):
        print("\n Όλα τα βιβλία στο σύστημα:")
        for _, row in self.dm.books_df.iterrows():
            print(f"[{row['id']}] {row['title']} by {row['author']} - {row['copies']} copies - {row['cost']} €")


    #υπολογισμος μεσης βαθμολογιας,Προβολη στατιστικων
    def show_book_statistics(self):
        print(" Στατιστικά Βιβλίων:")
    
        # Αντιγραφή για ασφαλή χρήση
        books = self.dm.books_df.copy()
    
        # Υπολογισμός μέσης βαθμολογίας
        books["average_rating"] = books["ratings"].apply(
    lambda r: round(np.mean(r), 2) if isinstance(r, list) and r else 0
    )


        
    
        # Προβολή πρώτων 5
        print(books[["title", "average_rating", "copies", "cost"]].head())
    
        # --- Γράφημα: Μέση Βαθμολογία ανά Βιβλίο ---
        plt.figure(figsize=(10, 5))
        plt.bar(books["title"], books["average_rating"], color='skyblue')
        plt.xticks(rotation=45, ha='right')
        plt.title(" Μέση Βαθμολογία Βιβλίων")
        plt.ylabel("Rating (0–5)")
        plt.tight_layout()
        plt.show()
    
        # --- Γράφημα: Αντίτυπα ανά Βιβλίο ---
        plt.figure(figsize=(10, 5))
        plt.bar(books["title"], books["copies"], color='green')
        plt.xticks(rotation=45, ha='right')
        plt.title(" Διαθέσιμα Αντίτυπα")
        plt.ylabel("Αριθμός Αντιτύπων")
        plt.tight_layout()
        plt.show()
    
        # --- Γράφημα: Πιο ακριβά βιβλία ---
        top_books = books.nlargest(5, "cost")
        plt.figure(figsize=(7, 7))
        plt.pie(top_books["cost"], labels=top_books["title"], autopct="%1.1f€")
        plt.title(" Τα 5 Πιο Ακριβά Βιβλία")
        plt.show()
        
      #Διαγραφη αξιολογησης  
    def delete_review(self, book_id):

        book_row = self.dm.books_df[self.dm.books_df["id"] == book_id]
        if book_row.empty:
            print(" Book not found.")
            return
    
        idx = book_row.index[0]
        ratings = self.dm.books_df.at[idx, "ratings"]
        if isinstance(ratings, str):
            ratings = ast.literal_eval(ratings)
    
        if not ratings:
            print(" No ratings to delete.")
            return
    
        print(f" Ratings for '{self.dm.books_df.at[idx, 'title']}': {ratings}")
        print("Ποιο review θέλεις να διαγράψεις;")
        for i, r in enumerate(ratings):
            print(f"{i + 1}.  {r}")
        print("0. Διαγραφή όλων")
    
        try:
            choice = int(input("Επιλογή: "))
            if choice == 0:
                ratings = []
                print("Όλες οι αξιολογήσεις διαγράφηκαν.")
            elif 1 <= choice <= len(ratings):
                removed = ratings.pop(choice - 1)
                print(f" Διαγράφηκε το rating: {removed}")
            else:
                print(" Μη έγκυρη επιλογή.")
                return
        except ValueError:
            print(" Μη έγκυρη είσοδος.")
            return
    
        self.dm.books_df.at[idx, "ratings"] = str(ratings)
        self.dm.save_data()
        print(" Ενημερώθηκε το βιβλίο.")
     #Προσθηκη βιβλιων απο CSV   
    def import_books_from_csv(self, filename):
    
        if not os.path.exists(filename):
            print(" Το αρχείο δεν υπάρχει.")
            return
    
        try:
            new_books = pd.read_csv(
                filename,
                converters={
                    "categories": ast.literal_eval,
                    "bookstores": ast.literal_eval,
                    "ratings": ast.literal_eval
                }
            )
        except Exception as e:
            print(" Σφάλμα κατά την ανάγνωση του CSV:", e)
            return
    
        # Προαιρετικός έλεγχος για διπλότυπα IDs
        existing_ids = self.dm.books_df["id"].tolist()
        new_books = new_books[~new_books["id"].isin(existing_ids)]
    
        if new_books.empty:
            print(" Δεν βρέθηκαν νέα βιβλία προς εισαγωγή.")
            return
    
        self.dm.books_df = pd.concat([self.dm.books_df, new_books], ignore_index=True)
        self.dm.save_data()
        print(f"Εισάχθηκαν {len(new_books)} νέα βιβλία από το {filename}.")
    
        
