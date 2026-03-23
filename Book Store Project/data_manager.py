import pandas as pd
import os

class DataManager:
    def __init__(self):
        self.users_file = "users.csv"
        self.admins_file = "admins.csv"
        self.books_file = "books.csv"
        self.user_df = pd.DataFrame()
        self.admin_df = pd.DataFrame()
        self.books_df = pd.DataFrame()

    def load_data(self):
        # Φορτώνουμε users.csv
        if os.path.exists(self.users_file):
            self.user_df = pd.read_csv(self.users_file, converters={
                "orders": eval,
                "favorites": eval
            })
        else:
            self.user_df = pd.DataFrame(columns=[
                "id", "username", "password", "address", "city",
                "orders", "favorites", "balance"
            ])

        # Φορτώνουμε admins.csv
        if os.path.exists(self.admins_file):
            self.admin_df = pd.read_csv(self.admins_file, converters={
                "bookstores": eval
            })
        else:
            self.admin_df = pd.DataFrame(columns=[
                "id", "username", "password", "bookstores"
            ])

        # Φορτώνουμε books.csv
        if os.path.exists(self.books_file):
            self.books_df = pd.read_csv(self.books_file, converters={
                "categories": eval,
                "bookstores": eval,
                "ratings": eval
            })

            # Αν λείπει η στήλη ratings → την προσθέτουμε
            if "ratings" not in self.books_df.columns:
                self.books_df["ratings"] = [[] for _ in range(len(self.books_df))]
        else:
            self.books_df = pd.DataFrame(columns=[
                "id", "title", "author", "publisher", "categories",
                "cost", "shipping_cost", "availability", "copies",
                "bookstores", "ratings"
            ])

    def save_data(self):
        print("SAVE_DATA FUNCTION LOADED!")

        print(" Saving data to CSV...")
        self.user_df.to_csv(self.users_file, index=False)
        self.admin_df.to_csv(self.admins_file, index=False)
        self.books_df.to_csv(self.books_file, index=False)

