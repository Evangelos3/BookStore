from data_manager import DataManager
from user_manager2 import UserManager
from admin_manager import AdminManager

def main():
    dm = DataManager()
    dm.load_data()

    um = UserManager(dm)
    am = AdminManager(dm)

    print("Καλώς ήρθατε στο σύστημα διαχείρισης βιβλιοπωλείου!")
    choice = input("1: Login\n2: Register\nΕπιλογή: ")

    if choice == "2":
        um.register_user()

    if choice in ["1", "2"]:
        if um.login_user():
            # Έλεγχος αν είναι admin (προαιρετικό)
            if um.current_user["username"] in dm.admin_df["username"].values:
                print(" Admin menu ενεργό.")
                am.admin_menu(um.current_user["id"])
            else:
                # User menu
                while True:
                    print("\n User Menu:")
                    print("1. Προβολή υπολοίπου")
                    print("2. Προβολή αγαπημένων")
                    print("3. Προσθήκη αγαπημένου")
                    print("4. Αφαίρεση αγαπημένου")
                    print("5. Διαθεσιμότητα και τιμή αγαπημένων")
                    print("6. Ενημέρωση προφίλ")
                    print("7. Αγορά βιβλίου")
                    print("8. Ακύρωση παραγγελίας")
                    print("9. Προβολή παραγγελιών")
                    print("10.Βαθμολογηση Βιβλιου")
                    print("11.Προβολη Αξιολογησης Βιβλιου")
                    print("12.Προτασεις Βιβλιων")
                    print("0. Έξοδος")
                    option = input("Επιλογή: ")

                    if option == "1":
                        um.check_balance()
                    elif option == "2":
                        um.show_favorites()
                    elif option == "3":
                        book_id = int(input(" Book ID για προσθήκη: "))
                        um.add_to_favorites(book_id)
                    elif option == "4":
                        book_id = int(input(" Book ID για αφαίρεση: "))
                        um.remove_from_favorites(book_id)
                    elif option == "5":
                        um.show_favorites_availability_and_price()
                    elif option == "6":
                        um.update_profile()
                    elif option == "7":
                        book_id = int(input(" Book ID για αγορά: "))
                        um.buy_book(book_id)
                    elif option == "8":
                        book_id = int(input(" Book ID για ακύρωση: "))
                        um.cancel_order(book_id)
                    elif option == "9":
                        um.show_orders()
                    elif option == "10":
                        book_id = int(input(" Book ID για αξιολόγηση: "))
                        um.rate_book(book_id)
                    elif option == "11":
                        book_id = int(input(" Book ID για προβολή αξιολόγησης: "))
                        um.show_book_rating(book_id)
                    elif option == "12":
                        um.suggest_books()
                    elif option == "0":
                        print(" Έξοδος από το σύστημα.")
                        break
                    else:
                        print(" Μη έγκυρη επιλογή.")

    dm.save_data()

if __name__ == "__main__":
    main()
