import streamlit as st
import json
import os


class BookCollection:
    """A class to manage a collection of books, allowing users to store and organize their reading materials."""

    def __init__(self):
        """Initialize a new book collection with an empty list and set up file storage."""
        self.storage_file = "books_data.json"
        if 'book_list' not in st.session_state:
            st.session_state.book_list = self.read_from_file()

    def read_from_file(self):
        """Load saved books from a JSON file into memory.
        If the file doesn't exist or is corrupted, start with an empty collection."""
        try:
            with open(self.storage_file, "r") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_to_file(self):
        """Store the current book collection to a JSON file for permanent storage."""
        with open(self.storage_file, "w") as file:
            json.dump(st.session_state.book_list, file, indent=4)

    def create_new_book(self, title, author, year, genre, is_read):
        """Add a new book to the collection by gathering information from the user."""
        new_book = {
            "title": title,
            "author": author,
            "year": year,
            "genre": genre,
            "read": is_read,
        }
        st.session_state.book_list.append(new_book)
        self.save_to_file()
        return True

    def delete_book(self):
        """Remove a book from the collection using its title."""
        book_title = input("Enter the title of the book to remove: ")

        for book in st.session_state.book_list:
            if book["title"].lower() == book_title.lower():
                st.session_state.book_list.remove(book)
                self.save_to_file()
                print("Book removed successfully!\n")
                return
        print("Book not found!\n")

    def find_book(self):
        """Search for books in the collection by title or author name."""
        search_type = input("Search by:\n1. Title\n2. Author\nEnter your choice: ")
        search_text = input("Enter search term: ").lower()
        found_books = [
            book
            for book in st.session_state.book_list
            if search_text in book["title"].lower()
            or search_text in book["author"].lower()
        ]

        if found_books:
            print("Matching Books:")
            for index, book in enumerate(found_books, 1):
                reading_status = "Read" if book["read"] else "Unread"
                print(
                    f"{index}. {book['title']} by {book['author']} ({book['year']}) - {book['genre']} - {reading_status}"
                )
        else:
            print("No matching books found.\n")

    def update_book(self):
        """Modify the details of an existing book in the collection."""
        book_title = input("Enter the title of the book you want to edit: ")
        for book in st.session_state.book_list:
            if book["title"].lower() == book_title.lower():
                print("Leave blank to keep existing value.")
                book["title"] = input(f"New title ({book['title']}): ") or book["title"]
                book["author"] = (
                    input(f"New author ({book['author']}): ") or book["author"]
                )
                book["year"] = input(f"New year ({book['year']}): ") or book["year"]
                book["genre"] = input(f"New genre ({book['genre']}): ") or book["genre"]
                book["read"] = (
                    input("Have you read this book? (yes/no): ").strip().lower()
                    == "yes"
                )
                self.save_to_file()
                print("Book updated successfully!\n")
                return
        print("Book not found!\n")

    def show_all_books(self):
        """Display all books in the collection with their details."""
        if not st.session_state.book_list:
            st.write("Your collection is empty.")
            return

        st.write("### Your Book Collection:")
        for index, book in enumerate(st.session_state.book_list, 1):
            reading_status = "Read" if book["read"] else "Unread"
            st.write(f"{index}. {book['title']} by {book['author']} ({book['year']}) - {book['genre']} - {reading_status}")

    def show_reading_progress(self):
        """Calculate and display statistics about your reading progress."""
        total_books = len(st.session_state.book_list)
        completed_books = sum(1 for book in st.session_state.book_list if book["read"])
        completion_rate = (
            (completed_books / total_books * 100) if total_books > 0 else 0
        )
        print(f"Total books in collection: {total_books}")
        print(f"Reading progress: {completion_rate:.2f}%\n")

    def start_application(self):
        """Run the main application loop with a user-friendly menu interface."""
        while True:
            print("📚 Welcome to Your Book Collection Manager! 📚")
            print("1. Add a new book")
            print("2. Remove a book")
            print("3. Search for books")
            print("4. Update book details")
            print("5. View all books")
            print("6. View reading progress")
            print("7. Exit")
            user_choice = input("Please choose an option (1-7): ")

            if user_choice == "1":
                self.create_new_book()
            elif user_choice == "2":
                self.delete_book()
            elif user_choice == "3":
                self.find_book()
            elif user_choice == "4":
                self.update_book()
            elif user_choice == "5":
                self.show_all_books()
            elif user_choice == "6":
                self.show_reading_progress()
            elif user_choice == "7":
                self.save_to_file()
                print("Thank you for using Book Collection Manager. Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.\n")


def main():
    st.title("📚 Book Collection Manager")
    
    book_manager = BookCollection()

    # Sidebar for navigation
    menu_choice = st.sidebar.selectbox(
        "Choose an option",
        ["View All Books", "Add New Book", "Search Books", "View Reading Progress","Delete a Book"]

    )

    if menu_choice == "Add New Book":
        st.header("Add a New Book")
        with st.form("new_book_form"):
            title = st.text_input("Book Title")
            author = st.text_input("Author")
            year = st.text_input("Publication Year")
            genre = st.text_input("Genre")
            is_read = st.checkbox("Have you read this book?")
            
            submit_button = st.form_submit_button("Add Book")
            if submit_button and title and author:
                book_manager.create_new_book(title, author, year, genre, is_read)
                st.success("Book added successfully!")

    elif menu_choice == "View All Books":
        book_manager.show_all_books()

    elif menu_choice == "Search Books":
        st.header("Search Books")
        search_term = st.text_input("Enter search term").lower()
        if search_term:
            found_books = [
                book for book in st.session_state.book_list
                if search_term in book["title"].lower() or search_term in book["author"].lower()
            ]
            if found_books:
                st.write("### Matching Books:")
                for book in found_books:
                    reading_status = "Read" if book["read"] else "Unread"
                    st.write(f"{book['title']} by {book['author']} ({book['year']}) - {book['genre']} - {reading_status}")
            
            else:
                st.write("No matching books found.")

    elif menu_choice == "View Reading Progress":
        st.header("Reading Progress")
        total_books = len(st.session_state.book_list)
        completed_books = sum(1 for book in st.session_state.book_list if book["read"])
        completion_rate = (completed_books / total_books * 100) if total_books > 0 else 0
        
        st.metric("Total Books", total_books)
        st.metric("Books Read", completed_books)
        st.progress(completion_rate / 100)
        st.write(f"Completion Rate: {completion_rate:.2f}%")
    elif menu_choice == "Delete a Book":
        st.header("Delete a Book")
        book_title = st.text_input("Enter the title of the book to remove")
        if st.button("Delete Book"):
            for book in st.session_state.book_list:
                if book["title"].lower() == book_title.lower():
                    st.session_state.book_list.remove(book)
                    book_manager.save_to_file()
                    st.success("Book removed successfully!")
                    break
            else:
                st.error("Book not found!")


if __name__ == "__main__":
    main()
