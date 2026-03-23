#  Python Bookstore Management System (CLI)

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Pandas](https://img.shields.io/badge/pandas-data%20manipulation-150458.svg)
![Matplotlib](https://img.shields.io/badge/matplotlib-visualization-orange.svg)

##  Overview
This is a comprehensive, Command-Line Interface (CLI) application for managing an electronic bookstore. Built entirely in Python, it utilizes `pandas` for robust data manipulation and persistent CSV storage, alongside `matplotlib` for generating administrative data visualizations.

The system supports two distinct user roles: **Administrators** and **Customers (Users)**, each with their own dedicated menus and capabilities.

##  Key Features

###  User (Customer) Features:
* **Account Management:** Secure registration and login with password validation (requires >=8 chars and special characters).
* **Virtual Wallet:** Users start with a virtual balance to purchase books.
* **Shopping Cart & Orders:** Buy books, check availability, and cancel orders for a full refund.
* **Favorites List:** Add/remove books to a personal favorites list and quickly check their current prices and availability.
* **Ratings & Reviews:** Rate purchased books (1-5 stars).
* **Smart Recommendations:** An algorithm suggests new books based on the most common categories found in the user's favorites list.

###  Administrator Features:
* **Inventory Management:** Add new books, update stock (copies), modify prices, or completely remove books from the system.
* **Bulk Import:** Import multiple books simultaneously via external CSV files.
* **Review Moderation:** View and delete specific user ratings/reviews.
* **Data Visualization & Statistics:** Automatically generates interactive charts using `matplotlib`:
  * Bar charts for Average Book Ratings.
  * Bar charts for Available Copies per Book.
  * Pie charts highlighting the Top 5 Most Expensive Books.

##  Project Structure
The application follows a modular Object-Oriented design:
* `main2.py`: The entry point of the application. Handles routing and the main interactive loop.
* `data_manager.py`: Acts as the database layer. Handles loading and saving data to `users.csv`, `admins.csv`, and `books.csv` using Pandas.
* `user_manager2.py`: Contains the `UserManager` class, handling all customer-facing logic and transactions.
* `admin_manager.py`: Contains the `AdminManager` class, handling inventory control and data visualization.

##  Prerequisites & Installation

To run this project locally, you need Python installed on your machine along with a few external libraries.

