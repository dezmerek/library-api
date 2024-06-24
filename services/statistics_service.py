from db import db
from models.reservation import Reservation
from models.book import Book
from bson import ObjectId
from datetime import datetime
from collections import Counter


def get_active_reservations_count():
    try:
        count = Reservation.collection.count_documents({"status": "active"})
        return {"count": count}
    except Exception as e:
        return {"msg": f"Błąd podczas pobierania liczby aktywnych rezerwacji: {str(e)}"}


def get_most_reserved_books(limit=5):
    try:
        pipeline = [
            {"$match": {"status": "active"}},
            {"$group": {"_id": "$book_id", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}},
            {"$limit": limit}
        ]

        results = list(Reservation.collection.aggregate(pipeline))
        most_reserved_books = []

        for result in results:
            book = Book.collection.find_one({"_id": result["_id"]})
            if book:
                most_reserved_books.append({
                    "book_id": str(result["_id"]),
                    "title": book["title"],
                    "author": book["author"],
                    "count": result["count"]
                })

        return most_reserved_books
    except Exception as e:
        return {"msg": f"Błąd podczas pobierania najczęściej rezerwowanych książek: {str(e)}"}
