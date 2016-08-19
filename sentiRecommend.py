from sentimentAnalysis import sentiAnalysis
from recommendation import recommendation
import numpy as np
class sentiRecommend:
    def __init__(self,maxRows,scoreThreshold):
        self.maxRows = maxRows
        self.recommendationSystem = recommendation(self.maxRows,0.1,4.2,"A1OTSX3JOCZH6K")
        self.recUserID = "A1OTSX3JOCZH6K"
        self.sentiObject = sentiAnalysis()
        self.scoreThreshold = scoreThreshold
        self.sentiRecommendations = []
        #self.recommend(self.recUserID)

    def getOriginalListIndex(self,curRID,curPID):
        for rIndex in range(0,self.maxRows):
            if (self.recommendationSystem.reviewerID[rIndex] == curRID):
                if(self.recommendationSystem.asin[rIndex] == curPID):
                    return rIndex
        
    def recommend(self,recUserID):
        self.recUserID = recUserID
        self.recommendationSystem = recommendation(self.maxRows,0.1,4.2,recUserID)
        self.recommendationSystem.getCurrentCluster()
        similarUsers = self.recommendationSystem.curCluster
        sentiRatings = []        
        if len(similarUsers) > 0:
            for rID in similarUsers:
                for pID in self.recommendationSystem.utilityMatrix[rID]:
                    reviewTextIndex = self.getOriginalListIndex(rID,pID)
                    reviewTextScore = self.sentiObject.computeScore(self.recommendationSystem.reviewText[reviewTextIndex])                    
                    sentiRatings.append(reviewTextScore)
                    if (reviewTextScore > self.scoreThreshold):
                        self.sentiRecommendations.append(pID) 
        else:
            for rID in list(set(self.recommendationSystem.reviewerID)):
                for pID in self.recommendationSystem.utilityMatrix[rID]:
                    reviewTextIndex = self.getOriginalListIndex(rID,pID)
                    reviewTextScore = self.sentiObject.computeScore(self.recommendationSystem.reviewText[reviewTextIndex])                                    
                    sentiRatings = sentiRatings.append(reviewTextScore)
                    if (reviewTextScore > self.scoreThreshold):
                        self.sentiRecommendations.append(pID)
        print "Recommendations for reviewer ID " + self.recUserID + ":",self.sentiRecommendations
        return np.mean(sentiRatings)

    def predictRating(self,recProductID):
        collectedRatings = []
        self.recommendationSystem.getCurrentCluster()
        similarUsers = self.recommendationSystem.curCluster
        sentiRatings = []        
        if len(similarUsers) > 0:
            for rID in similarUsers:
                reviewTextIndex = self.getOriginalListIndex(rID,recProductID)
                if reviewTextIndex is not None: 
                    reviewTextScore = self.sentiObject.computeScore(self.recommendationSystem.reviewText[reviewTextIndex])                    
                    sentiRatings.append(reviewTextScore)                
        else:
            for rID in list(set(self.recommendationSystem.reviewerID)):            
                reviewTextIndex = self.getOriginalListIndex(rID,recProductID)
                if reviewTextIndex is not None: 
                    reviewTextScore = self.sentiObject.computeScore(self.recommendationSystem.reviewText[reviewTextIndex])                                    
                    sentiRatings = sentiRatings.append(reviewTextScore)                
        if (len(sentiRatings) > 0):
            return np.mean(sentiRatings,axis=0)
        else:
            return 0
        
        
