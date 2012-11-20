import json
from graphFunc import *
class store:
    def __init__(self, obj):
        self.storeId = obj["business_id"]
        # This represents set of reviewers
        self.reviewers = []
        self.reliability = 1
        self.reviewers = set()
        self.reviews = set()
    def display(self):
        print self.storeId, self.reliability, self.reviews
    def addtuples(self, tuple_list):
        self.reviewers = set([a[1] for a in tuple_list])
        self.reviews = set([a[0] for a in tuple_list])
    def values(self):
        """
        Returns a list of all the values inside a store obj
        """
        return [ str(s) for s in [self.storeId, self.reliability]]
    def calc_reliability(self, review_map, reviewer_map):
        theta = 0
        global verbose
        if verbose:
            print "Store_id", self.storeId
        for review_id in self.reviews:
            curr_reviewer = review_map[review_id].reviewerId
            curr_trust = reviewer_map[curr_reviewer].trustiness
            if curr_trust > 0:
                theta += ((review_map[review_id].rating-3)*curr_trust)
                if verbose:
                    print "review rating = ", review_map[review_id].rating-3
                    print "curr_trust = ", curr_trust
                    print "theta = ", theta
        R = normalise(theta)
        if verbose:
            print "Final Theta = ", theta
            print "R = ", R
        self.reliability = R

class reviewer:
    """
    Contains all the data relating to a reviewer
    """
    def __init__(self, obj):
        self.reviewerId = obj["user_id"]
        self.trustiness = 1
        # This represents the list of tuples (reviewId, storeId)
        self.reviews = set()
        self.feedback = obj["votes"]
    def display(self):
        print self.reviewerId, self.trustiness, self.reviews
    def addtuples(self, review_list):
        self.reviews = review_list
    def values(self):
        """
        Returns a list of all the values inside a reviewer
        """
        return [ str(s) for s in [self.reviewerId, self.trustiness,\
                                  self.feedback]]
    def calc_trustiness(self, review_map):
        H = 0
        for review_id in self.reviews:
            H += review_map[review_id].honesty
        T = normalise(float(H))
        if verbose: 
            print "Trustiness", self.reviewerId
            print "H = ", H
            print "T = ", T 
        self.trustiness = T

class review:
    """
    The review class represents the review
    It stores all the data relating to a review
    """
    def __init__(self, obj):
        self.reviewId = obj["review_id"]
        self.reviewerId = obj["user_id"]
        self.storeId = obj["business_id"]
        self.text = obj["text"]
        self.rating = obj["stars"]
        self.date = obj["date"]
        self.feedback = obj["votes"]
        self.agreement = 1
        self.honesty = 1
    def calc_honesty(self, reviewer_map):
        self.honesty = abs(reviewer_map[self.reviewerId].trustiness)*self.agreement
        global verbose
        if verbose:
            print "honesty", self.reviewId
            print "honesty = ", self.agreement, "*",\
                abs(reviewer_map[self.reviewerId].trustiness), " = ",\
                self.honesty

    def calc_agreement(self, review_map, reviewer_map, store_map):
        t_agr = 0
        t_dis = 0
        global verbose
        for review_id in store_map[self.storeId].reviews:
            if abs(review_map[review_id].rating - self.rating) <= 1:
                t_agr += \
                    reviewer_map[review_map[review_id].reviewerId].trustiness
            else:
                t_dis += \
                reviewer_map[review_map[review_id].reviewerId].trustiness
        A = float(t_agr - t_dis)
        An = normalise(A)
        if verbose:
            print "Agreement", self.reviewId
            print "A = ", A
            print "An = ", An
        self.agreement = An
    
    def display(self):
        print self.reviewId, self.date, self.feedback, self.rating,\
                self.reviewerId,\
                self.storeId, self.agreement, self.honesty
    def values(self, reviewer_map, store_map):
        """
        Returns a list of all the values inside a review
        """

        return [ str(s) for s in [self.reviewId, self.feedback, self.rating,\
                                  self.reviewerId, self.storeId, self.agreement,\
                                  self.honesty,\
                                  reviewer_map[self.reviewerId].trustiness,\
                                  store_map[self.storeId].reliability]]

