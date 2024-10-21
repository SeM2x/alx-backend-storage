#!/usr/bin/env python3
"""module that defines update_topics function"""


def update_topics(mongo_collection, name, topics):
    """changes all topics of a school document based on the name"""
    mongo_collection.update_many({"name": name}, {"$set": {"topics": topics}})
