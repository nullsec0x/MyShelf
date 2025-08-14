# MyShelf: A Personal Book Collection Manager

MyShelf is a web-based application built with Flask that allows users to manage their personal book collections. Users can add, view, edit, and delete books, as well as search for books using the Google Books API.

**Creator:** nullsec0x

This project was developed to meet common web application requirements, including robust user authentication, comprehensive CRUD (Create, Read, Update, Delete) functionality, and seamless integration with external APIs.

## Features

*   User authentication (signup, login, logout)
*   Add new books to your collection
*   Edit existing book details
*   Delete books from your collection
*   View details of individual books
*   Search for books using the Google Books API to pre-fill book information

## Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/nullsec0x/MyShelf.git
    cd myshelf
    ```

2.  **Create a virtual environment and activate it:**

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install the required dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the application:**

    ```bash
    python app.py
    ```

    The application will run on `http://127.0.0.1:5000/`.

## Usage

1.  **Sign Up / Login:** Navigate to the application in your browser. You will be prompted to log in or sign up for a new account.
2.  **Add Books:** Once logged in, you can add new books to your collection by clicking the "Add New Book" button. You can manually enter details or use the "Search Google Books" feature to auto-fill information.
3.  **Manage Books:** From your book collection, you can view details, edit, or delete books.

## Screenshots

| Feature | Screenshot |
|---|---|
| Login Page | ![Login Page](https://i.postimg.cc/Y9ftS7HF/Screenshot-20250814-085237.png) |
| Empty Book Collection | ![Empty Book Collection](https://i.postimg.cc/TYkYmTWq/Screenshot-20250814-085257.png) |
| Add New Book Form | ![Add New Book Form](https://i.postimg.cc/PqDtBZV2/Screenshot-20250814-085305.png) |
| Search Google Books | ![Search Google Books](https://i.postimg.cc/JnW1mn9m/Screenshot-20250814-085323.png) |
| Book Added Successfully | ![Book Added Successfully](https://i.postimg.cc/JzG75SNw/Screenshot-20250814-085334.png) |
| Book Details | ![Book Details](https://i.postimg.cc/pXVLpmyL/Screenshot-20250814-085343.png) |


