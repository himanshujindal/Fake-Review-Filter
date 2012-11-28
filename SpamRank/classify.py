import json
from sklearn import svm
from sklearn.feature_extraction.text import TfidfVectorizer
import os
from sklearn.naive_bayes import GaussianNB, BernoulliNB, MultinomialNB
from sklearn.linear_model import LogisticRegression
# Take as input
#   spam_list - a list of string containing spam reviews
#   nonspam_list - a list of string containing nonspam reviews
#   test - a list of string containing strings to be tested
# Returns as output
#   a list of numbers representing the class of test strings
YELP_DATASET = "/Users/himanshujindal/Documents/Stony Brook/3rd Sem/Data Mining/Yelp Data/yelp_academic_dataset.json"
def get_numbers(spam_list, nonspam_list, test, classifier):
    corpus = spam_list + nonspam_list
    print "Training data size: ", len(corpus)
    vectorizer = TfidfVectorizer(min_df=1)
    X = vectorizer.fit_transform(corpus).toarray()
    Y = [1]*len(spam_list) + [0]*len(nonspam_list)
    # clf = LogisticRegression(penalty='l1')
    clf = classifier()
    clf.fit(X, Y)
    return_list = []
    len(test)
    for test_data in test:
        return_list.append([clf.predict_proba(vectorizer.transform([test_data]).toarray())])
        if len(return_list)%1000 == 0:
            print len(return_list)
    print "Returning data test size: ", len(return_list)
    return return_list

# Fuction to test the get_numbers fn
def test_driver(classifier):
    fold_list = ['fold1', 'fold2', 'fold3', 'fold4', 'fold5']
    path_spam = '/Users/himanshujindal/Documents/Stony Brook/3rd Sem/Data Mining/op_spam_v1.3/MTurk'
    path_nonspam = '/Users/himanshujindal/Documents/Stony Brook/3rd Sem/Data Mining/op_spam_v1.3/TripAdvisor'
    spam = []
    for fold in fold_list:
        for file in os.listdir(path_spam+'/'+fold):
            spam.append(open(path_spam+'/'+fold+'/'+file, 'r').read())
    print "Read", len(spam), "spam docs"
    nonspam = []
    for fold in fold_list:
        for file in os.listdir(path_nonspam+'/'+fold):
            nonspam.append(open('/'.join((path_nonspam, fold, file)), 'r').read())
    print "Read", len(nonspam), "Non spam docs"
    test = []
    f = open(YELP_DATASET, 'r')
    for line in f:
        obj = json.loads(line)
        if obj["type"] == "review":
            test.append(obj["text"])
    print "Testing Spam articles", len(test)
    test_arr = get_numbers(spam, nonspam, test, classifier)
    for row in test_arr:
        z = row[0][0]
        x += z[0]
        y += z[1]
    print x, y
def otherfunc():
    test = []
    for data in test:
        test.append(open('/'.join((path_spam, fold_list[-1], file)), 'r').read())
    test_arr = get_numbers(spam, nonspam, test, classifier)
    # print "1 ", test_arr.count(1)
    # print "0 ", test_arr.count(0)
    x = 0
    y = 0
    for row in test_arr:
        z = row[0][0]
        x += z[0]
        y += z[1]
    print x, y
    
    # for row in test_arr:
    #     print row
    test = []
    print "Testing Non Spam articles"
    for file in os.listdir(path_nonspam+'/'+fold_list[-1]):
        test.append(open('/'.join((path_nonspam, fold_list[-1], file)), 'r').read())
    test_arr = get_numbers(spam, nonspam, test, classifier)
    # print "1 ", test_arr.count(1)
    # print "0 ", test_arr.count(0)
    x = 0
    y = 0
    for row in test_arr:
        z = row[0][0]
        x += z[0]
        y += z[1]
    print x, y

#print "GaussianNB"
#test_driver(GaussianNB)
#print "MultinomialNB"
#test_driver(MultinomialNB)
print "BernoulliNB"
test_driver(BernoulliNB)
#print "Logistic Regression"
#test_driver(LogisticRegression)
