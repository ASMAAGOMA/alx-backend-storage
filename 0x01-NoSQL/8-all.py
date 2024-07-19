#!/usr/bin/env python3
"""
list all docs
"""


def list_all(mongo_collection):
    """
    list all docs
    """
    return [docs for docs in mongo_collection.find()]
