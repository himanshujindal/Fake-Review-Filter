import csv
import json
class review:
    def __init__(self, obj, reviewer_tuple, store_tuple):
        self.review_id = obj['ReviewId']
        self.feedback = obj['Feedback']
        self.rating = obj['Rating']
        self.agreement = obj['Agreement']
        self.reliability = obj['Reliability']
        self.honesty = obj['Honesty']
        self.trustiness = obj['Trustiness']
        self.store_avgrating = store_tuple[1]
        self.store_numreviews = store_tuple[0]
        self.reviewer_numreviews = reviewer_tuple[0]
        self.reviewer_avgrating = reviewer_tuple[1]
        self.reviewer_feedback = reviewer_tuple[2] 
    def display(self, writer):
        writer.writerow((str(self.review_id), str(self.feedback),
                        str(self.rating), str(self.agreement),
                        str(self.honesty), 
                        str(self.reliability), str(self.trustiness),
                        str(self.store_avgrating), str(self.store_numreviews),
                        str(self.reviewer_avgrating),
                         str(self.reviewer_numreviews),
                        str(self.reviewer_feedback)))
f = open('yelp_academic_dataset.json', 'r')
store_map = {}
reviewer_map = {}
for line in f:
    obj = json.loads(line)
    if obj["type"] == "business":
        store_map[obj['business_id']] = (obj['review_count'], obj['stars'])
    if obj["type"] == "user":
        reviewer_map[obj['user_id']] = (obj['review_count'], obj['average_stars'], obj['votes'])
f = open('review_map.csv', 'r')
reader = csv.DictReader(f)
review_map = {}
for row in reader:
    review_map[row['ReviewId']] = review(row, reviewer_map[row['ReviewerId']],\
                                         store_map[row['StoreId']])
f.close()
f = open('results.csv', 'w')
writer = csv.writer(f)
writer.writerow(('ReviewId', 'Feedback', 'Rating', 'Agreement', 'Honesty',\
                'Reliability', 'Trustiness', 'store_avg_rating',\
                'store_numreviews', 'reviewer_avg_rating',\
                'reviewer_num_reviews',\
                'reviewer_feedback'))
for review in review_map:
    review_map[review].display(writer)
f.close()
