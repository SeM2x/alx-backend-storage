#!/usr/bin/env python3
"""module that defines list_all function"""


def list_all(mongo_collection):
    """lists all documents in a collection"""
    return mongo_collection.find()
