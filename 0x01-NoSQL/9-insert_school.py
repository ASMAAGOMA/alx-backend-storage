#!/usr/bin/env python3
"""
insert
"""


def insert_school(mongo_collection, **kwargs):
    """
    insert
    """
    hmm = mongo_collection.insert_one(kwargs)
    return hmm.inserted_id
