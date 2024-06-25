from db import db
from datetime import datetime, UTC
from bson.objectid import ObjectId


class Review:
    collection = db.reviews

    @staticmethod
    def to_json(review):
        return {
            "review_id": str(review["_id"]),
            "book_id": str(review["book_id"]),
            "user_id": str(review["user_id"]),
            "rating": review["rating"],
            "comment": review.get("comment", ""),
            "created_at": review["created_at"].isoformat()
        }

    @classmethod
    def create(cls, book_id, user_id, rating, comment=""):
        review = {
            "book_id": ObjectId(book_id),
            "user_id": ObjectId(user_id),
            "rating": rating,
            "comment": comment,
            "created_at": datetime.now(UTC)
        }
        cls.collection.insert_one(review)
        return cls.to_json(review)

    @classmethod
    def get_by_book(cls, book_id):
        reviews = cls.collection.find({"book_id": ObjectId(book_id)})
        return [cls.to_json(review) for review in reviews]

    @classmethod
    def get_all(cls):
        reviews = cls.collection.find()
        return [cls.to_json(review) for review in reviews]
