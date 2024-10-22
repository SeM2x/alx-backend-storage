#!/usr/bin/env python3
"""script that provides some stats about Nginx logs stored in MongoDB"""
from pymongo import MongoClient


if __name__ == '__main__':
    client = MongoClient('mongodb://127.0.0.1:27017')
    nginx_logs_collection = client.logs.nginx
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]

    doc_count = nginx_logs_collection.count_documents({})

    print("{} logs".format(doc_count))
    print("Methods:")
    for method in methods:
        method_count = nginx_logs_collection.count_documents(
            {"method": method})
        print("\tMethod {}: {}".format(method, method_count))

    status_count = nginx_logs_collection.count_documents(
        {"method": "GET", "path": "/status"})
    print("{} status check".format(status_count))
