from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
from config import DATABASE_CONFIG
from scipy.spatial.distance import euclidean
import pandas as pd
import numpy as np

app = Flask(__name__)
app.secret_key = 'ablsghecg'

def get_db_connection():
    connection = mysql.connector.connect(**DATABASE_CONFIG)
    return connection

def insert_manual_data(username, password):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
    connection.commit()
    cursor.close()
    connection.close()

def get_user_details(username):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT password, id FROM users WHERE username = %s", (username,))
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    if result:
        return result[0], result[1]
    else:
        return None, None

def fetch_books_data():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT id, booktitle, author, image_url, average_rating, num_ratings FROM books")
    books_data = cursor.fetchall()
    cursor.close()
    connection.close()
    return books_data

def fetch_fav_books_data(id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT id, booktitle, author, image_url, average_rating, num_ratings FROM books WHERE id = %s",(id,))
    books_data = cursor.fetchall()
    cursor.close()
    connection.close()
    return books_data

def fetch_book_details_by_id(book_id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT id as book_id, booktitle, author, image_url, average_rating, num_ratings FROM books WHERE id = %s", (book_id,))
    book_data = cursor.fetchone()
    cursor.close()
    connection.close()
    return book_data

def insert_new_book(booktitle, author, image_url, average_rating, num_ratings):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO books (booktitle, author, image_url, average_rating, num_ratings) VALUES (%s, %s, %s, %s, %s)",
                   (booktitle, author, image_url, average_rating, num_ratings))
    connection.commit()
    cursor.close()
    connection.close()

def insert_user_book_rating(user_id, book_id, rating):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO user_books (user_id, book_id, rating) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE rating = %s",
                   (user_id, book_id, rating, rating))
    connection.commit()
    cursor.close()
    connection.close()

def get_user_rated_book_ids(user_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    query = """
    SELECT book_id
    FROM user_books
    WHERE user_id = %s
    ORDER BY rating DESC
    """
    cursor.execute(query, (user_id,))
    rated_book_ids = [row[0] for row in cursor.fetchall()]
    cursor.close()
    connection.close()
    return rated_book_ids

def create_ratings_dataframe():
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT DISTINCT id FROM books ORDER BY id ASC")
    book_ids = [row[0] for row in cursor.fetchall()]
    print(book_ids)

    cursor.execute("SELECT DISTINCT id FROM users ORDER BY id ASC")
    user_ids = [row[0] for row in cursor.fetchall()]
    print(user_ids)

    ratings_df = pd.DataFrame(index=book_ids, columns=user_ids)

    cursor.execute("SELECT user_id, book_id, rating FROM user_books")
    ratings = cursor.fetchall()

    for user_id, book_id, rating in ratings:
        ratings_df.at[book_id, user_id] = rating

    cursor.close()
    connection.close()

    ratings_df = ratings_df.fillna(0)
    print(ratings_df)

    return ratings_df


def find_similar_books(book_id, df):
    book_ratings = df.loc[book_id]
    df = df.drop(book_id)

    similar_books = []
    for idx, row in df.iterrows():
        common_ratings_mask = (book_ratings != 0) & (row != 0)
        if np.any(common_ratings_mask):
            distance = euclidean(book_ratings[common_ratings_mask], row[common_ratings_mask])
            similar_books.append((idx, distance))

    similar_books.sort(key=lambda x: x[1])
    similar_book_ids = [book_id for book_id, _ in similar_books[:4]]

    return similar_book_ids


def remove_duplicates(B):
    seen = set()
    result = []

    for item in B:
        if item not in seen:
            seen.add(item)
            result.append(item)

    return result

def get_sub_books(v):
    res = []
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    for a in v:
        tmp = "SELECT id FROM books WHERE LOWER(booktitle) LIKE '%"
        tmp += a.lower()
        tmp += "%'"
        print(tmp)
        cursor.execute(tmp)
        book_data = cursor.fetchall()
        print("book data[all]: ")
        for b in book_data:
            print(b['id'])
            res.append(b['id'])
        # print(book_data[0]['id'])
    cursor.close()
    connection.close()
    res=remove_duplicates(res)
    print("res: ")
    print(res)
    return res

def get_rating_num(id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(
        "SELECT AVG(rating) as a, COUNT(book_id) as b FROM user_books WHERE book_id = %s",
        (id,))
    book_data = cursor.fetchall()
    print("here")
    print(book_data[0]['a'],book_data[0]['b'])
    cursor.close()
    connection.close()
    return book_data[0]['a'], book_data[0]['b']

def name_of_book(a):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(
        "SELECT booktitle FROM books WHERE id = %s",
        (a,))
    book_data = cursor.fetchall()
    # print("name of book id")
    # print(book_data[0]['booktitle'])
    cursor.close()
    connection.close()
    return book_data[0]['booktitle']

def find_related_books(s):
    v = s.split()
    v=remove_duplicates(v)
    res = get_sub_books(v)
    return res

@app.route('/')
def home():
    if 'username' in session:
        fav_books = get_user_rated_book_ids(session['user_id'])
        fav_books = fav_books[:4]
        print(fav_books)
        a, b = get_rating_num(4)
        print("ekhane ")
        print(a, b)
        # v= "harry the"
        # find_related_books(v)
        ratings_df = create_ratings_dataframe()
        # print("first rating df")
        # print(ratings_df)
        similar_books = []
        from_which = {}
        print("konta theke konta")
        # print(fav_books)
        for a in fav_books:
            b=find_similar_books(a,ratings_df)
            # print(a, "theke")
            # print(b)
            # print("similar to ", a)
            # print(b)
            for c in b:
                if c not in from_which:
                    # name_of_book(a)
                    from_which[c]=name_of_book(a)
                similar_books.append(c)
        similar_books = remove_duplicates(similar_books)

        print(from_which)
        # similar_books = find_similar_books(6,ratings_df)
        # print(similar_books)
        book_data = []
        rating = {}
        num_ratings = {}
        # i = 0
        for a in similar_books:
            b=fetch_fav_books_data(a)
            # print(b)
            print("what ",b[0]['id'])
            c, d = get_rating_num(b[0]['id'])
            rating[a]=c
            num_ratings[a]=d
            book_data.append(b[0])
            # book_data[i]['']
            # i+=1
        print("final now")
        print(rating)
        print(num_ratings)
        print("book data")
        print(book_data);
        # print(ratings_df)
        # print(find_related_books("hello my hello name is sayeef"))

        return render_template('home.html', username=session['username'],books=book_data,rating=rating,num_ratings=num_ratings, from_which=from_which)
    else:
        return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        stored_password, user_id = get_user_details(username)

        if stored_password is None:
            print("User not registered")
        elif stored_password == password:
            print("Login success")
            session['username'] = username
            session['user_id'] = user_id
            print(f"User ID stored in session: {user_id}")
            return redirect(url_for('home'))
        else:
            print("Incorrect Password")

    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if get_user_details(username)[0]:
            print("User already exists")
        else:
            print("Signup success")
            insert_manual_data(username, password)

        return redirect(url_for('login'))

    return render_template('signup.html')

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('username', None)
    session.pop('user_id', None)
    return redirect(url_for('login'))

@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if 'username' in session:
        if request.method == 'POST':
            booktitle = request.form['booktitle']
            author = request.form['author']
            image_url = request.form['image_url']
            # average_rating = float(request.form['average_rating'])
            # num_ratings = int(request.form['num_ratings'])

            insert_new_book(booktitle, author, image_url, 0, 0)
            return redirect(url_for('browse_books'))

        return render_template('add_book.html')
    else:
        return redirect(url_for('login'))

@app.route('/browse_books', methods=['GET', 'POST'])
def browse_books():
    if 'username' in session:
        books_data = fetch_books_data()
        print("here now")
        print(books_data)

        rating = {}
        num_ratings = {}
        # i = 0
        for a in books_data:
            # b = fetch_fav_books_data(a['id'])
            # print(b)
            print("what ", a['id'])
            c, d = get_rating_num(a['id'])
            rating[a['id']] = c
            num_ratings[a['id']] = d
        # s = request.form['query']
        # print("query ",s)
        return render_template('browse_books.html', books=books_data, rating=rating, num_ratings=num_ratings)
    else:
        return redirect(url_for('login'))

@app.route('/book_detail/<int:book_id>')
def book_detail(book_id):
    if 'username' in session:
        book = fetch_book_details_by_id(book_id)
        print("now we are here ")
        print(book)
        # rating = {}
        # num_ratings = {}
        # i = 0
        # for a in book:
            # b = fetch_fav_books_data(a['id'])
            # print(b)
        print("what ", book['book_id'])
        c, d = get_rating_num(book['book_id'])
        # rating[book['book_id']] = c
        # num_ratings[book['book_id']] = d
        if book:
            return render_template('book_detail.html', book=book, rating=c, num_ratings=d)
        else:
            return render_template('error.html', message='Book not found')
    else:
        return redirect(url_for('login'))

@app.route('/search_books', methods=['GET', 'POST'])
def search_books():
    if 'username' in session:
        s = request.args.get('query', '')
        # print(s)
        v = find_related_books(s)
        book_data = []
        rating = {}
        num_ratings = {}
        for a in v:
            b = fetch_fav_books_data(a)
            print("now we are here 2 ")
            print(b)
            c, d = get_rating_num(b[0]['id'])
            rating[a] = c
            num_ratings[a] = d
            book_data.append(b[0])
        print(book_data)
        # print(v)

        # i = 0
        # for a in v:
        #     b = fetch_fav_books_data(a)
        #     # print(b)
        #     print("what ", b[0]['id'])
        #     c, d = get_rating_num(b[0]['id'])
        #     rating[a] = c
        #     num_ratings[a] = d
        #     # book_data.append(b[0])

        return render_template('search_books.html',books=book_data, s=s, rating=rating, num_ratings=num_ratings)
    else:
        return redirect(url_for('login'))


@app.route('/submit_rating', methods=['POST'])
def submit_rating():
    if 'username' in session:
        user_id = session['user_id']
        # print("userid ",user_id)
        book_id = request.form['book_id']
        rating = request.form['rating']
        print(f"User ID: {user_id}, Book ID: {book_id}, Rating: {rating}")
        insert_user_book_rating(user_id, book_id, rating)
        return redirect(url_for('book_detail', book_id=book_id))
    else:
        return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True,port=4558)
