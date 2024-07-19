#!/usr/bin/env python3
"""
update names
"""


def update_topics(mongo_collection, name, topics):
    """
    update names
    """
    mongo_collection.update_many(
        {"name": name},
        {"$set": {"topics": topics}}
    )
