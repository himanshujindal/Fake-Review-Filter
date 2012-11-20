import sys
import json
from optparse import OptionParser

def parse_opt():
    parser = OptionParser()
    parser.add_option("-n", "--num", dest="num", type="int", \
                                        help="Number of reviews in subset")
    parser.add_option("-v", "--verbose",
                                        action="store_true", dest="verbose",
                      default=False,
                                        help="Specify for verbose mode")
    (options, args) = parser.parse_args()
    return options.num, options.verbose

if __name__ == '__main__':
    N, verbose = parse_opt()
    print N
    f = open('yelp_academic_dataset.json', 'r')
    reviews = 0
    users = set()
    business = set()
    f_w = open('yelp_subset.json', 'w')
    for line in f:
        obj = json.loads(line)
        if reviews >= N:
            break
        elif obj["type"] == "review":
            f_w.write("%s\n"%(json.dumps(obj)))
            reviews += 1
            print reviews
            users.add(obj["user_id"])
            business.add(obj["business_id"])
    f.close()
    print reviews
    print len(users)
    print len(business)
    f = open('yelp_academic_dataset.json', 'r')
    for line in f:
        obj = json.loads(line)
        if obj["type"] == "user" and obj["user_id"] in users:
            f_w.write("%s\n"%(json.dumps(obj)))
        elif obj["type"] == "business" and obj["business_id"] in business:
            f_w.write("%s\n"%(json.dumps(obj)))
    f_w.close()
    f.close()
