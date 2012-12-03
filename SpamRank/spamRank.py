#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python
# -*- coding: utf-8 -*-
import os
import json
from sklearn import svm
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import GaussianNB, BernoulliNB, MultinomialNB
from sklearn.linear_model import LogisticRegression
import networkx as nx
import datetime
import itertools
import matplotlib.pyplot as plt
# Using the Yelp dataset for spam analysis
# Pseudogold std dataset provided by Myle Ott is used to classify
# This returns
#   review_map - A dictionary of review_id to review obj
#   store_map - A dictionary of store_id to set containing reviews for same
#               store
#   reviewer_map - A dictionaryof reviewer_id to set containing reviews from
#                   same reviewers
YELP_DATASET = "/Users/himanshujindal/Documents/Stony Brook/3rd Sem/Data Mining/Yelp Data/yelp_academic_dataset.json"
# YELP_DATASET = "/Users/himanshujindal/Documents/Stony Brook/3rd Sem/Data Mining/Yelp Data/yelp_subset.json"
SPAM_DATA = "/Users/himanshujindal/Documents/Stony Brook/3rd Sem/Data Mining/op_spam_v1.3/MTurk"
NONSPAM_DATA = "/Users/himanshujindal/Documents/Stony Brook/3rd Sem/Data Mining/op_spam_v1.3/TripAdvisor"
# Take as input
#   spam_list - a list of string containing spam reviews
#   nonspam_list - a list of string containing nonspam reviews
#   test - a list of string containing strings to be tested
# Returns as output
#   a list of numbers representing the class of test strings
def get_numbers(spam_list, nonspam_list, test):
    corpus = spam_list + nonspam_list
    print "Training data size: ", len(corpus)
    vectorizer = TfidfVectorizer(min_df=1)
    X = vectorizer.fit_transform(corpus).toarray()
    Y = [1]*len(spam_list) + [0]*len(spam_list)
    # clf = LogisticRegression(penalty='l1')
    clf = BernoulliNB()
    clf.fit(X, Y)
    print "Data Fitted. Predicting reviews: ", len(test)
    return_list = []
    for data in test:
        result = clf.predict_proba(\
                    vectorizer.transform(\
                    [data]).toarray())[0][1]
        return_list.append(result)
    print "Returning data test size: ", len(return_list)
    return return_list

def edge_metric(num):
    return 1/(1+(float(num)/30))

class review:
    def __init__(self, obj):
        self.review_id = obj["review_id"]
        self.reviewer_id = obj["user_id"]
        self.store_id = obj["business_id"]
        self.text = obj["text"]
        self.date = obj["date"]
        self.rating = obj["stars"]
        self.spamrank = 0
        self.connections = {}
        self.temp = 0
    def display(self):
        print self.review_id, ",", self.spamrank
    def distance(self, review2):
        date1 = self.date
        date2 = review2.date
        dist = edge_metric(difference(date1, date2))
        return dist
    def add_edge(self, review2, dist):
        self.connections[review2] = dist
    def getrank(self):
        self.temp = 0
        for review in self.connections:
            self.temp+= (review.spamrank*self.connections[review]/len(review.connections))
        if not self.connections:
            self.temp = self.spamrank
    def swaptemp(self):
        self.spamrank = self.temp

def difference(date1_str, date2_str):
    date1 = datetime.datetime.strptime(date1_str, "%Y-%m-%d")
    date2 = datetime.datetime.strptime(date2_str, "%Y-%m-%d")
    diff_date = abs(date1-date2)
    return diff_date.days

def processFile(currentDir):
    """ 
    Read all text files within this directory
    Returns a list of string representing the files read
    """
    return_list = []
    currentDir = os.path.abspath(currentDir)
    filesInCurDir = os.listdir(currentDir)
    for file in filesInCurDir:
        curFile = os.path.join(currentDir, file)
        if os.path.isfile(curFile):
            curFileExtension = curFile[-3:]
            if curFileExtension == 'txt':
                return_list.append(open(curFile, 'r').read())
        else:
            return_list.extend(processFile(curFile))
    return return_list

def grab_data_yelp():
    f = open(YELP_DATASET, 'r')
    review_map = {}
    reviewer_map = {}
    store_map = {}
    for line in f:
        obj = json.loads(line)
        if obj["type"] == "review":
            # review_map
            review_map[obj["review_id"]] = review(obj)
            # reviewer_map
            reviewer_map.setdefault(obj["user_id"], [])
            reviewer_map[obj["user_id"]].append(obj["review_id"]) 
            # store_map
            store_map.setdefault(obj["business_id"], [])
            store_map[obj["business_id"]].append((obj["review_id"]))
    return review_map, reviewer_map, store_map

def get_data():
    spam_list = processFile(SPAM_DATA)
    nonspam_list = processFile(NONSPAM_DATA)
    review_map, reviewer_map, store_map = grab_data_yelp()
    review_list = [[review_map[review_id].review_id, \
                    review_map[review_id].text] \
                   for review_id in review_map]
    review_scores = get_numbers(spam_list, nonspam_list, \
                                [ obj[1] for obj in review_list])
    for row in zip(review_list, review_scores):
        review_map[row[0][0]].spamrank = row[1]
    return review_map, reviewer_map, store_map

def spamrank():
    review_map, reviewer_map, store_map = get_data()
    print "review objects and dicts"
    for reviewer_id in reviewer_map:
        pairs = itertools.permutations(reviewer_map[reviewer_id], 2)
        for item in pairs:
            review1 = review_map[item[0]]
            review2 = review_map[item[1]]
            dist = review1.distance(review2)
            review1.add_edge(review2, dist)
            review2.add_edge(review1, dist)
    print "Added edge for reviewers"
    print len(store_map)
    for store_id in store_map:
        pairs = itertools.permutations(store_map[store_id], 2)
        for item in pairs:
            review1 = review_map[item[0]]
            review2 = review_map[item[1]]
            dist = review1.distance(review2)
            if abs(review1.rating - review2.rating) <= 1:
                review1.add_edge(review2, dist)
                review2.add_edge(review1, dist)
    print "Added edge for stores"
    for i in range(4):
        print "ITERATION", i+1
        for review_id in review_map:
            review_map[review_id].display()
            review_map[review_id].getrank()
        for review_id in review_map:
            review_map[review_id].swaptemp()
    for review_id in review_map:
        review_map[review_id].display()

spamrank()
