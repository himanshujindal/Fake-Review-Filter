import json
from graphClasses import review, reviewer, store
def grab_data_yelp(file):
    global verbose
    f = open(file, 'r')
    review_map = {}
    reviewer_map = {}
    store_map = {}
    date_map = {}
    reviewer2review_map = {}
    store2review_map = {}
    for line in f:
        obj = json.loads(line)
        if obj["type"] == "review":
            #review_map
            review_map[obj["review_id"]] = review(obj)
            #date_map
            date_map.setdefault(obj["date"], [])
            date_map[obj["date"]].append(obj["review_id"])
            #reviewer2review_map
            reviewer2review_map.setdefault(obj["user_id"], [])
            reviewer2review_map[obj["user_id"]].append(obj["review_id"]) 
            #store2review_map
            store2review_map.setdefault(obj["business_id"], [])
            store2review_map[obj["business_id"]].append((obj["review_id"],\
                                                         obj["user_id"]))
        elif obj["type"] == "user":
            reviewer_map[obj["user_id"]] = reviewer(obj)
        elif obj["type"] == "business":
            store_map[obj["business_id"]] = store(obj)
    for reviewer_id in reviewer2review_map:
        reviewer_map[reviewer_id].addtuples(reviewer2review_map[reviewer_id])
    for store_id in store2review_map:
        store_map[store_id].addtuples(store2review_map[store_id])
    print len(review_map), len(reviewer_map), len(store_map), len(date_map)
    return review_map, reviewer_map, store_map, date_map

