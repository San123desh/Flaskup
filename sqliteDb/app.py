from flask import Flask, request, jsonify
import json
import sqlite3

app = Flask(__name__)

def db_connection():
    conn = None
    try:
        conn = sqlite3.connect('books.sqlite')
    except sqlite3.error as e:
        print(f"The error '{e}' occurred")
    return conn

@app.route('/books', methods=['GET', 'POST'])
def books():
    # grab the db connection
    conn = db_connection()
    cursor = conn.cursor()

    if request.method == 'GET':
        cursor = conn.execute("SELECT * FROM book")
        books = [
            dict(id=row[0], author=row[1],publication_year=row[2],title=row[3])
            for row in cursor.fetchall()
        ]
        if books is not None:
            return jsonify(books), 200

    if request.method == 'POST':
            new_author = request.json['author']
            publication_year = request.json['publication_year']
            title = request.json['title']
            sql = """INSERT INTO book (author, publication_year, title) VALUES (?,?,?)"""
            cursor.execute(sql, (new_author, publication_year, title))
            conn.commit()
            return jsonify({"message": "Book added successfully"}), 201
    

@app.route('/book/<int:id>', methods=['GET','PUT','DELETE'])
def single_book(id):
    conn = db_connection()
    cursor = conn.cursor()
    book = None
    if request.method == 'GET':
        cursor.execute("SELECT * FROM book WHERE id=?",(id,))
        rows = cursor.fetchall()
        for r in rows:
            book = r
        if book is not None:
            return jsonify(book), 200
        else:
            return jsonify({"error": "Book not found"}), 404

    
    if request.method == 'PUT':
            sql = """UPDATE book SET title=?, publication_year=?,author=? WHERE id=?"""

            data = request.json  # Fetch the JSON data from the request
            author = data['author']
            publication_year = data['publication_year']
            title = data['title']
            updated_book = {
                "id": id,
                "author": author,
                "title": title,
                "publication_year": publication_year
            }
            conn.execute(sql, (author, publication_year, title,id))
            conn.commit()
            return jsonify(updated_book), 200
    
    
    if request.method == 'DELETE':
        sql = """DELETE FROM book WHERE id=?"""
        conn.execute(sql, (id,) )
        conn.commit()
        return jsonify({"message": "Book deleted successfully"}), 204
    

if __name__ == '__main__':
    app.run()
