from flask import Flask, request, jsonify

app = Flask(__name__)

books_list = [
    {"id": 0, "author": "Author 1", "title": "Book 1", "publication_year": 2000},
    {"id": 1, "author": "Author 2", "title": "Book 2", "publication_year": 2005},
    {"id": 2, "author": "Author 3", "title": "Book 3", "publication_year": 2010}
]

@app.route('/books', methods=['GET', 'POST'])
def books():
    if request.method == 'GET':
        if books_list:
            return jsonify(books_list)
        else:
            return jsonify({"error": "Nothing found"}), 404

    if request.method == 'POST':
        if not request.is_json:
            return jsonify({"error": "Unsupported Media Type"}), 415

        try:
            new_author = request.json['author']
            title = request.json['title']
            publication_year = request.json['publication_year']
        except KeyError as e:
            return jsonify({"error": f"Missing key: {str(e)}"}), 400

        iD = books_list[-1]['id'] + 1 if books_list else 0
        new_book = {"id": iD, "author": new_author, "title": title, "publication_year": publication_year}

        books_list.append(new_book)
        return jsonify(new_book), 201
    

@app.route('/book/<int:id>', methods=['GET','PUT','DELETE'])
def single_book(id):
    if request.method == 'GET':
        for book in books_list:
            if book['id'] == id:
                return jsonify(book)
        return jsonify({"error":"Book not found"}), 404
    
    if request.method == 'PUT':
        updated_data = request.get_json()
        for book in books_list:
            if book['id'] == id:
                book['author'] = updated_data.get('author', book['author'])
                book['title'] = updated_data.get('title', book['title'])
                book['publication_year'] = updated_data.get('publication_year', book['publication_year'])
                update_book = {
                    "id": id,
                    "author": book['author'],
                    "title": book['title'],
                    "publication_year": book['publication_year']
                }
                return jsonify(update_book), 200
        return jsonify({"error":"Book not found"}), 404
    
    if request.method == 'DELETE':
        for i, book in enumerate(books_list):
            if book['id'] == id:
                books_list.pop(i)
                return jsonify({"message": "Book deleted"}), 204
        return jsonify({"error": "Book not found"}), 404



if __name__ == '__main__':
    app.run()
