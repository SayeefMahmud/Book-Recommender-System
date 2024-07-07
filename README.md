# Book-Recommender-System

## This is a book recommender website where users can add and rate books and receive recommendations of related books based on their ratings.

Welcome to the Book Recommender System! This project is a web application designed to enhance your reading experience by providing personalized book recommendations. Built using Python and the Flask framework, along with HTML, JavaScript, and CSS for the front end, this system allows users to add and rate books. The application leverages the XAMPP database to store and manage book information and user ratings. Based on these ratings, users receive recommendations for related books that align with their preferences. Dive into a curated selection of books tailored just for you!

## Features

- **User Authentication**:
  - **Sign Up**: New users can create an account.
  - **Log In**: Returning users can log in to access their personalized features.

- **Book Management**:
  - **Add Books**: Users can add new books to the database.
  - **Browse Books**: Users can browse through the collection of books available on the platform.

- **Book Ratings and Recommendations**:
  - **Rate Books**: Users can rate books they have read.
  - **Personalized Recommendations**: Based on their ratings, users get personalized book recommendations.

- **External Links**:
  - **Search for Books**: Each book has a link that redirects to an Amazon.com search page with the name of the book.


## Setup Instructions

1. Install the dependencies - Numpy, Pandas, Flask, XAMPP.
2. Clone this project.
3. Start the servers in XAMPP. Navigate to http://localhost/phpmyadmin/ . Create a new database for the Book Recommender System. Use the provided SQL file to set up the database schema. The SQL file is located in the `database` directory of the repository. Insert sample data to test the application.
4. Update the `config.py` file with the appropriate database name.
5. Run the `app.py` Python file by ```python app.py```. The Book Recommender website will now be accessible at  http://127.0.0.1:4558 .
6. Sign Up or Log in to browse books.
