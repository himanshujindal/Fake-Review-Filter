import csv, json, sys

input = open(sys.argv[1], 'r')

review_f = csv.writer(open('review.csv', 'w'))
reviewer_f = csv.writer(open('reviewer.csv', 'w'))
store_f = csv.writer(open('store.csv', 'w'))

review = 0
user = 0
business = 0
for line in input:
    obj = json.loads(line)
    try:
        if obj["type"] == "review":
            if review == 0:
                review_f.writerow(obj.keys())  # header row
            review_f.writerow([str(s).encode("utf-8") for s in obj.values()])
            review += 1
        if obj["type"] == "business":
            if business == 0:
                store_f.writerow(obj.keys())  # header row
            store_f.writerow([str(s).encode("utf-8") for s in obj.values()])
            business += 1
        if obj["type"] == "user":
            if user == 0:
                reviewer_f.writerow(obj.keys())  # header row
            reviewer_f.writerow([str(s).encode("utf-8") for s in obj.values()])
            user += 1
    except UnicodeEncodeError:
        pass
input.close()
