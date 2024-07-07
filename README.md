# Book-Recommender-System

## This is a book recommender website where users can add and rate books and receive recommendations of related books based on their ratings.

Welcome to the Book Recommender System! This project is a web application designed to enhance your reading experience by providing personalized book recommendations. Built using Python and the Flask framework, along with HTML, JavaScript, and CSS for the front end, this system allows users to add and rate books. The application leverages the XAMPP database to store and manage book information and user ratings. Based on these ratings, users receive recommendations for related books that align with their preferences. Dive into a curated selection of books tailored just for you!

## Features

- **User Authentication**:
  - **Sign Up**: New users can create an account.
  - **Log In**: Returning users can log in to access their personalized features.

- **Book Management**:
  - **Add Books**: Users can add new books to the website.
  - **Browse Books**: Users can browse through the collection of books available on the platform.

- **Book Ratings and Recommendations**:
  - **Rate Books**: Users can rate books they have read.
  - **Personalized Recommendations**: Based on their ratings, users get personalized book recommendations.

- **External Links**:
  - **Buy Books**: Each book has a link that redirects to Amazon.com where users can buy the book.


## Setup Instructions

1. Install the dependencies:
   - Install Numpy, Pandas, and Flask by running the command `pip install numpy pandas flask`
   - Install XAMPP from https://www.apachefriends.org/
3. Clone this project.
4. Start the servers in XAMPP. Navigate to http://localhost/phpmyadmin/ . Create a new database for the Book Recommender System. Use the `userdb.sql` file to set up the database schema, the SQL file is located in the `database` directory of the repository.
5. Update the `config.py` file with the appropriate database name.
6. Run the `app.py` Python file by ```python app.py```. The Book Recommender website will now be accessible at  http://127.0.0.1:4558 .
7. Sign Up or Log in to browse books.
