#!/usr/bin/env python3
"""
find element by topic
"""


def schools_by_topic(mongo_collection, topic):
    """
    find element by topic
    """
    match = {
        "topics": {
            "$elemMatch": {
                "$eq": topic,
            },
        },
    }
    return [docs for docs in mongo_collection.find(match)]
