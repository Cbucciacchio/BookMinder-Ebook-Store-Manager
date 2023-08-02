#============================Imports=============================
import sqlite3

#============================DATABASE============================
db = sqlite3.connect('ebookstore_db')
cursor = db.cursor()  # Get a cursor object

#creating the table 'books'
cursor.execute('''
    CREATE TABLE IF NOT EXISTS books(id INTEGER PRIMARY KEY, Title TEXT,
                   	Author TEXT, Qty INTEGER)
''')
db.commit()

#populating the table
cursor = db.cursor()

id1 = 3001
Title1 = 'A Tale of Two Cities'
Author1 = 'Charles Dickens'
Qty1 = 30

id2 = 3002
Title2 = 'Harry Potter and the Philosopher s Stone'
Author2 = 'J.K. Rowling'
Qty2 = 40

id3 = 3003
Title3 = 'The Lion, the Witch and the Wardrobe'
Author3 = 'C. S. Lewis'
Qty3 = 25

id4 = 3004
Title4 = 'The Lord of the Rings'
Author4 = 'J.R.R Tolkien'
Qty4 = 37

id5 = 3005
Title5 = 'Alice in Wonderland'
Author5 = 'Lewis Carroll'
Qty5 = 12

# Insert student 1
cursor.execute('''INSERT INTO books(id, Title, Author, Qty)
                  VALUES(?,?,?,?)''', (id1, Title1, Author1, Qty1))
print('First book inserted')

# Insert student 2
cursor.execute('''INSERT INTO books(id, Title, Author, Qty)
                  VALUES(?,?,?,?)''', (id2, Title2, Author2, Qty2))
print('Second book inserted')

# Insert student 3
cursor.execute('''INSERT INTO books(id, Title, Author, Qty)
                  VALUES(?,?,?,?)''', (id3, Title3, Author3, Qty3))
print('Third book inserted')

# Insert student 4
cursor.execute('''INSERT INTO books(id, Title, Author, Qty)
                  VALUES(?,?,?,?)''', (id4, Title4, Author4, Qty4))
print('Fourth book inserted')

# Insert student 5
cursor.execute('''INSERT INTO books(id, Title, Author, Qty)
                  VALUES(?,?,?,?)''', (id5, Title5, Author5, Qty5))
print('Fifth book inserted')

db.commit()

#============================Functions===========================
def enter_book():
    """
    Allows the user to enter a new book and add it to the database.
    """
    try:
        # Get input from the user
        id = int(input("Enter the book ID: "))
        title = input("Enter the book title: ")
        author = input("Enter the author's name: ")
        quantity = int(input("Enter the book quantity: "))

        # Create a new Book object with the provided details
        new_book = Book(id, title, author, quantity)

        # Insert the book into the database
        cursor.execute('''INSERT INTO books(id, Title, Author, Qty)
                          VALUES(?,?,?,?)''', (new_book.get_id(), new_book.get_title(), new_book.get_author(), new_book.get_quantity()))
        db.commit()

        print("Book successfully added to the database.")
    except ValueError:
        print("Invalid input. Please enter valid values for ID and Quantity.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")


def update_book():
    """
    Allows the user to update information about a book.
    """
    try:
        book_id = int(input("Enter the ID of the book you want to update: "))

        # Check if the book with the provided ID exists in the database
        cursor.execute("SELECT * FROM books WHERE id=?", (book_id,))
        book_data = cursor.fetchone()

        if book_data is None:
            print("Book not found in the database.")
        else:
            print("\nCurrent Book Details:")
            print(Book(*book_data))

            # Ask the user for the field they want to update
            print("\nWhat information would you like to update?")
            print("1. Title")
            print("2. Author")
            print("3. Quantity")
            choice = int(input("Enter your choice (1/2/3): "))

            # Update the selected field based on the user's choice
            if choice == 1:
                new_title = input("Enter the new title: ")
                cursor.execute("UPDATE books SET Title=? WHERE id=?", (new_title, book_id))
                print("Title updated successfully.")
            elif choice == 2:
                new_author = input("Enter the new author: ")
                cursor.execute("UPDATE books SET Author=? WHERE id=?", (new_author, book_id))
                print("Author updated successfully.")
            elif choice == 3:
                new_quantity = int(input("Enter the new quantity: "))
                cursor.execute("UPDATE books SET Qty=? WHERE id=?", (new_quantity, book_id))
                print("Quantity updated successfully.")
            else:
                print("Invalid choice. Please choose a number between 1 and 3.")

            db.commit()
    except ValueError:
        print("Invalid input. Please enter valid values.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")


def delete_book():
    """
    Allows the user to delete a book from the database.
    """
    try:
        book_id = int(input("Enter the ID of the book you want to delete: "))

        # Check if the book with the provided ID exists in the database
        cursor.execute("SELECT * FROM books WHERE id=?", (book_id,))
        book_data = cursor.fetchone()

        if book_data is None:
            print("Book not found in the database.")
        else:
            print("\nBook Details:")
            print(Book(*book_data))

            # Confirm the deletion with the user
            confirmation = input("Are you sure you want to delete this book? (yes/no): ")

            if confirmation.lower() == "yes":
                # Delete the book from the database
                cursor.execute("DELETE FROM books WHERE id=?", (book_id,))
                print("Book deleted successfully.")
                db.commit()
            else:
                print("Deletion canceled.")
    except ValueError:
        print("Invalid input. Please enter a valid book ID.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")


def search_book():
    """
    Allows the user to search for a book in the database based on title or author.
    """
    try:
        search_option = int(input("Search by:\n1. Title\n2. Author\nEnter your choice (1/2): "))

        if search_option == 1:
            title_search = input("Enter the book title: ")
            cursor.execute("SELECT * FROM books WHERE Title LIKE ?", ('%' + title_search + '%',))
        elif search_option == 2:
            author_search = input("Enter the author's name: ")
            cursor.execute("SELECT * FROM books WHERE Author LIKE ?", ('%' + author_search + '%',))
        else:
            print("Invalid choice. Please enter 1 or 2.")
            return

        books_found = cursor.fetchall()

        if not books_found:
            print("No books found matching your search.")
        else:
            print("\nBooks Found:")
            for book_data in books_found:
                print(Book(*book_data))
    except ValueError:
        print("Invalid input. Please enter a valid choice.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")


#============================Classes=============================
class Book:
    """
    A class to represent a Book.

    Attributes
    ----------
    id : int
        The id number of the book
    Title : str
        The title of the book
    Author : str
        The name of the Author of the book 
    quantity : int
        The quantity of the shoe
    """

    def __init__(self, id, title, author, quantity):
        """Initializes the book with provided values."""

        self.id = id
        self.title = title
        self.author = author
        self.quantity = quantity
        
    def get_id(self):
        """Return the id of the book."""
        return self.id

    def get_title(self):
        """Return the title of the book."""
        return self.title
    
    def get_author(self):
        """Return the author of the book."""
        return self.author
        
    def get_quantity(self):
        """Return the quantity of the book."""
        return self.quantity

    def __str__(self):
        """
        Returns a string representation of a book with all attributes.
        """
        return f" ID: \t\t {self.id}\n Title: \t {self.title}\n Author: \t {self.author}\n Quantity: \t {self.quantity}\n"
        
#============================Main Menu===========================

def main():
    """
    Handles the main loop of the program. Provides an interface for user interaction.
    """
    choice = 1
    while choice != 0:
        print("\n1. Enter book")
        print("2. Update book ")
        print("3. Delete book ")
        print("4. Search books ")
        print("0. Exit")
        choice = int(input("Enter your choice: "))

        if choice == 1:
            enter_book()
        elif choice == 2:
            update_book()
        elif choice == 3:
            delete_book()
        elif choice == 4:
            search_book()
        elif choice == 0:
            cursor.execute('''DROP TABLE books''')
            db.commit()
            db.close()
            print("Closing the app..............Bye thank you!")
        else:
            print("Invalid choice. Please choose a number between 0 and 4.")

if __name__ == "__main__":
    main()
