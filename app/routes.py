from app import db
from flask import Blueprint
from flask import request
from flask import jsonify
from .models.book import Book


books_bp = Blueprint("books", __name__, url_prefix="/books")

def is_int(value):
    try:
        return int(value)
    except ValueError:
        return False




@books_bp.route("/<book_id>", methods=["GET"], strict_slashes=False)
def get_single_book(book_id):
    # Try to find the book with the given id

    if not is_int(book_id):
        return {
            "message": f"ID {book_id} must be an integer",
            "success": False
        }, 400

    book = Book.query.get(book_id)

    if book:
        return book.to_json(), 200
    
    return {
        "message": f"Book with id {book_id} was not found",
        "success": False,
    }, 404

@books_bp.route("", methods=["GET"], strict_slashes=False)
def books_index():
    books = Book.query.all()
    books_response = []
    for book in books:
        books_response.append(book.to_json() )
    
    return jsonify(books_response), 200

@books_bp.route("", methods=["POST"], strict_slashes=False)
def books():
    request_body = request.get_json()
    new_book = Book(title = request_body["title"],
                        description = request_body["description"])
    
    db.session.add(new_book)
    db.session.commit()

    return {
        "success": True,
        "message": f"Book {new_book.title} has been created"
    }, 201





# hello_world_bp = Blueprint("hello_world", __name__)

# @hello_world_bp.route('/hello-world', methods=["GET"])
# def get_hello_world():
#     my_response = "Hello, World!"
#     return my_response

# @hello_world_bp.route('/hello-world/JSON', methods=["GET"])
# def hello_world_json():
#     return {
#         "name": "Simon!",
#         "message": "Heya!",
#         "hobbies": ["Coding", "Writing", "Subversive Politics"],
#     }, 404


# @hello_world_bp.route("/broken-endpoint-with-broken-server-code")
# def broken_endpoint():
#     response_body = {
#         "name": "Ada Lovelace",
#         "message": "Hello!",
#         "hobbies": ["Fishing", "Swimming", "Watching Reality Shows"]
#     }
#     new_hobby = "Surfing"
#     response_body["hobbies"] + [new_hobby]
#     return response_body
