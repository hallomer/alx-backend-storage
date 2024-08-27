#!/usr/bin/env python3
"""provides some stats about Nginx logs and top IPs"""
from pymongo import MongoClient


def log_stats():
    """provides stats about Nginx logs stored in MongoDB"""
    client = MongoClient('mongodb://127.0.0.1:27017')
    db = client.logs
    collection = db.nginx

    log_count = collection.count_documents({})
    print(f"{log_count} logs")

    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    print("Methods:")
    for method in methods:
        method_count = collection.count_documents({"method": method})
        print(f"\tmethod {method}: {method_count}")

    status_check_count = collection.count_documents({
        "method": "GET", "path": "/status"
    })
    print(f"{status_check_count} status check")
    print("IPs:")
    ip_aggregation = collection.aggregate(
        [{"$group": {"_id": "$ip", "count": {"$sum": 1}}},
         {"$sort": {"count": -1}}])
    ip_counter = 0
    for ip_entry in ip_aggregation:
        if ip_counter == 10:
            break
        print(f"\t{ip_entry.get('_id')}: {ip_entry.get('count')}")
        ip_counter += 1


if __name__ == "__main__":
    log_stats()
