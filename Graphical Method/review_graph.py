import sys
import csv
from optparse import OptionParser
from graphFunc import *
from yelpData import grab_data_yelp

_DEL_T_ = 30
_ITER_NUM_ = 4
_REVIEW_HEADER_ = ["ReviewId", "Feedback", "Rating", "ReviewerId", "StoreId",\
                   "Agreement", "Honesty", "Trustiness", "Reliability"]
_REVIEWER_HEADER_ = ["ReviewerId", "Trustiness", "Feedback"]
_STORE_HEADER_ = ["StoreId", "Reliability"]

def parse_opt():
    """
    To parse the arguments
    Filename to parse and 
    verbose mode
    """
    global verbose
    parser = OptionParser()
    parser.add_option("-f", "--file", dest="file",\
                                        help="Name of Input file",
                      metavar="FILE")
    parser.add_option("-v", "--verbose",
                                        action="store_true", dest="verbose",
                      default=False,
                                        help="Specify for verbose mode")
    (options, args) = parser.parse_args()
    verbose = options.verbose
    return options.file


if __name__ == '__main__':
    print "grabbing yelp data"
    file = parse_opt()
    print file
    print verbose
    review_map, reviewer_map, store_map, date_map = grab_data_yelp(file)
    if verbose:
        print "Reviews"
        for review_id in review_map:
            review_map[review_id].display()
        print "Reviewers"
        for reviewer_id in reviewer_map:
            reviewer_map[reviewer_id].display()
        print "Store"
        for store_id in store_map:
            store_map[store_id].display()
    print "Done. Now iterating"
    for i in range(_ITER_NUM_):
        print "Iteration ", i
        print "Honesty"
        compute_honesty(review_map, reviewer_map, store_map)
        print "Trustiness"
        compute_trustiness(reviewer_map, review_map)
        print "Reliability"
        compute_reliability(store_map, review_map, reviewer_map)
    temp = sys.stdout
    review_f = csv.writer(open('review_map.csv', 'w'))
    reviewer_f = csv.writer(open('reviewer_map.csv', 'w'))
    store_f = csv.writer(open('store_map.csv', 'w'))
    review_f.writerow(_REVIEW_HEADER_)
    for review_id in review_map:
        review_f.writerow([str(s).encode("utf-8") for s in
                           review_map[review_id].values(reviewer_map, store_map)])
    reviewer_f.writerow(_REVIEWER_HEADER_)
    for reviewer_id in reviewer_map:
        reviewer_f.writerow([str(s).encode("utf-8") for s in
                           reviewer_map[reviewer_id].values()])
    store_f.writerow(_STORE_HEADER_)
    for store_id in store_map:
        store_f.writerow([str(s).encode("utf-8") for s in
                           store_map[store_id].values()])
