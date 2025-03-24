import json
import os
import random

def load_activities(mode="fun"):
    path = f"data/activities_{mode}.json"
    if not os.path.exists(path):
        print(f"Activity file not found for mode: {mode}")
        return []

    with open(path, "r") as f:
        return json.load(f)

def convert_time_to_activities(total_hours, activity_count=10, mode="fun"):
    activities = load_activities(mode)
    random.shuffle(activities)

    results = []
    used_activities = set()

    for item in activities:
        if item["activity"] in used_activities:
            continue  # Skip duplicates

        units = int(total_hours // item["hours"])
        if units > 0:
            results.append(f"- {item['activity'].capitalize()} {units} times")
            used_activities.add(item["activity"])

        if len(results) >= activity_count:
            break

    return results
