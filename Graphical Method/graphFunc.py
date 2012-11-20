import datetime
import math
verbose = False

def normalise(num):
    """
    Get the 2/e^num -1 for any num
    """
    try:
        return (2/(1+math.exp(-num)))-1
    # For very small value or very large values, there will be overflows,
    # In that case, we return -1 or 1
    except OverflowError:
        if num < 0:
            return -1
        else:
            return 1

def add_dates(inp_str, num):
    """
    Get the date num days before date represented by string inp_str
    """
    inp_date = datetime.datetime.strptime(inp_str, "%Y-%m-%d")
    op_date = inp_date + datetime.timedelta(days=num)
    return op_date.strftime("%Y-%m-%d")

def compute_honesty(review_map, reviewer_map, store_map):
    for review_id in review_map:
        review_map[review_id].calc_agreement(review_map, reviewer_map, store_map)
        review_map[review_id].calc_honesty(reviewer_map)

def compute_trustiness(reviewer_map, review_map):
    for reviewer_id in reviewer_map:
        reviewer_map[reviewer_id].calc_trustiness(review_map)

def compute_reliability(store_map, review_map, reviewer_map):
    for store_id in store_map:
        store_map[store_id].calc_reliability(review_map, reviewer_map)

