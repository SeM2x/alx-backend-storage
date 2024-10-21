#!/usr/bin/env python3
"""module that defines insert_school function"""


def insert_school(mongo_collection, **kwargs):
    """inserts a new documents in a collection"""
    return mongo_collection.insert_one(kwargs).inserted_id
