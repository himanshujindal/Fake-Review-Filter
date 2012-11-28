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
def get_numbers(spam_list, nonspam_list, test):
    corpus = spam_list + nonspam_list
    print "Training data size: ", len(corpus)
    vectorizer = TfidfVectorizer(min_df=1)
    X = vectorizer.fit_transform(corpus).toarray()
    Y = [1]*len(spam_list) + [0]*len(spam_list)
    # clf = LogisticRegression(penalty='l1')
    clf = BernoulliNB()
    clf.fit(X, Y)
    return_list = [[clf.predict_proba(vectorizer.transform([test_data]).toarray())] for test_data in test]
    print "Returning data test size: ", len(return_list)
    return return_list

# Fuction to test the get_numbers fn
def test_driver():
    fold_list = ['fold1', 'fold2', 'fold3', 'fold4', 'fold5']
    path_spam = '/Users/himanshujindal/Documents/Stony Brook/3rd Sem/Data Mining/op_spam_v1.3/MTurk'
    path_nonspam = '/Users/himanshujindal/Documents/Stony Brook/3rd Sem/Data Mining/op_spam_v1.3/TripAdvisor'
    spam = []
    for fold in fold_list[:-1]:
        for file in os.listdir(path_spam+'/'+fold):
            spam.append(open(path_spam+'/'+fold+'/'+file, 'r').read())
    print "Read", len(spam), "spam docs"
    nonspam = []
    for fold in fold_list[:-1]:
        for file in os.listdir(path_nonspam+'/'+fold):
            nonspam.append(open('/'.join((path_nonspam, fold, file)), 'r').read())
    print "Read", len(nonspam), "Non spam docs"
    test = []
    for file in os.listdir(path_spam+'/'+fold_list[-1]):
        test.append(open('/'.join((path_spam, fold_list[-1], file)), 'r').read())
    test_arr = get_numbers(spam, nonspam, test)
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
    for file in os.listdir(path_nonspam+'/'+fold_list[-1]):
        test.append(open('/'.join((path_nonspam, fold_list[-1], file)), 'r').read())
    test_arr = get_numbers(spam, nonspam, test)
    # print "1 ", test_arr.count(1)
    # print "0 ", test_arr.count(0)
    x = 0
    y = 0
    for row in test_arr:
        z = row[0][0]
        x += z[0]
        y += z[1]
    print x, y

test_driver()
