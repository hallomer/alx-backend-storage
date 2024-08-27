#!/usr/bin/env python3
"""inserts a new document in a collection"""


def insert_school(mongo_collection, **kwargs):
    """inserts a new document based on kwargs"""
    new = mongo_collection.insert_one(kwargs)
    return new.inserted_id
