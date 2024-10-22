#!/usr/bin/env python3
"""module that defines update_topics function"""


def top_students(mongo_collection):
    """returns all students sorted by average score"""
    students = mongo_collection.aggregate([
        {"$project": {"_id": 1, "name": 1, "averageScore": {
            "$avg": "$topics.score"}, "topics": 1}},
        {"$sort": {"averageScore": -1}}
    ])
    return students
