#!/usr/bin/env python3
"""module that defines update_topics function"""


def top_students(mongo_collection):
    """returns all students sorted by average score"""
    students = mongo_collection.aggregate([
        {"$unwind": "$topics"},
        {"$group": {"_id": "$_id", "averageScore": {"$avg": "$topics.score"}}},
        {"$sort": {"averageScore": -1}}
    ])
    return students

