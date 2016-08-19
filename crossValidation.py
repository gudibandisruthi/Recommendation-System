import random
from recommendation import recommendation
from sentiRecommend import sentiRecommend
import numpy as np
class crossValidate:
    def __init__(self,maxRows):
        self.numberOfFolds = 10
        self.testingSetSize = 100
        self.maxRows = maxRows
        self.foldSize = self.maxRows/self.numberOfFolds
        self.testingReviewerIDs = []
        self.testingProductIDs = []
        self.testingOriginalRatings = []
        self.testingPredictedRatings = []
        self.sentiPredictedRatings = []
        self.recommendationSystem = recommendation(self.maxRows,0.1,4.2,"A1OTSX3JOCZH6K")
        self.sentiObject = sentiRecommend(self.maxRows,3.5)
        self.tenfoldError()
    def refreshFoldObjets(self):
        self.testingReviewerIDs = []
        self.testingProductIDs = []
        self.testingOriginalRatings = []
        self.testingPredictedRatings = []
        self.sentiPredictedRatings = []
    def tenfoldError(self):
        print "Computing 10 fold error for ",self.maxRows,"review records..."
        totalRmse = []
        totalSentiRmse = []
        originalRatings = []
        self.reviewerList = list(self.recommendationSystem.utilityMatrix.keys())
        for foldIndex in range(self.numberOfFolds):            
            self.curReviewerList = self.reviewerList[foldIndex:foldIndex+self.foldSize]
            tIndex = 0
            self.refreshFoldObjets()
            for testingIndex in range(self.testingSetSize):
                curRevieweID = random.choice(self.reviewerList)
                if(curRevieweID is not None and self.recommendationSystem.utilityMatrix[curRevieweID] is not None):                    
                    curProductID = random.choice(self.recommendationSystem.utilityMatrix[curRevieweID].keys())
                    if(self.recommendationSystem.utilityMatrix[curRevieweID][curProductID] is not None and (curRevieweID not in self.testingReviewerIDs or curProductID not in self.testingProductIDs)):
                        self.testingProductIDs.append(curProductID)
                        self.testingReviewerIDs.append(curRevieweID)
                        self.testingOriginalRatings.append(self.recommendationSystem.utilityMatrix[curRevieweID][curProductID])
                        self.recommendationSystem.utilityMatrix[curRevieweID][curProductID] = None
            
            originalRatings = list(self.testingOriginalRatings)
            self.testingSetSize = len(self.testingReviewerIDs)
            predictedSetSize = 0
            for testingIndex in range(0,self.testingSetSize):
                self.recommendationSystem.recUserID = self.testingReviewerIDs[testingIndex]
                self.recommendationSystem.getCurrentCluster()
                predictedRating = self.recommendationSystem.predictRating(self.testingProductIDs[testingIndex])
                sentiPredictedRating = self.sentiObject.predictRating(self.testingProductIDs[testingIndex])
                if(predictedRating == 0 or sentiPredictedRating == 0):
                    self.testingOriginalRatings[testingIndex] = 0
                    self.sentiPredictedRatings.append(0)
                    self.testingPredictedRatings.append(0)                    
                else:
                    predictedSetSize = predictedSetSize + 1            
                    self.sentiPredictedRatings.append(sentiPredictedRating)
                    self.testingPredictedRatings.append(predictedRating)
            for index in range(len(self.testingReviewerIDs)):
                curRevieweID = self.testingReviewerIDs[index]
                curProductID = self.testingProductIDs[index]
                self.recommendationSystem.utilityMatrix[curRevieweID][curProductID] = self.testingOriginalRatings[index]
            rmseSum = 0
            rmse = 0
            sentiRmseSum = 0
            for testingIndex in range(0,self.testingSetSize):
                rmseSum = rmseSum + ((self.testingOriginalRatings[testingIndex] - self.testingPredictedRatings[testingIndex])*(self.testingOriginalRatings[testingIndex] - self.testingPredictedRatings[testingIndex]))                
                sentiRmseSum = sentiRmseSum + ((self.testingOriginalRatings[testingIndex] - self.sentiPredictedRatings[testingIndex])*(self.testingOriginalRatings[testingIndex] - self.sentiPredictedRatings[testingIndex]))
            rmse = np.sqrt(float(rmseSum / predictedSetSize))
            sentiRmse = np.sqrt(float(sentiRmseSum / predictedSetSize))
            totalRmse.append(rmse)
            totalSentiRmse.append(sentiRmse)
            print "Rmse by collaborative filtering method for fold",foldIndex+1,":",rmse
            print "Rmse by Sentiment analysis method for fold",foldIndex+1,":",sentiRmse
           
        avgRmse = np.mean(totalRmse)
        avgSentiRmse = np.mean(totalSentiRmse)
        print "Root mean square error for recommendations using collaborative filtering:",avgRmse
        print "Root mean square error for recommendations using sentimental analysis:",avgSentiRmse
        
        
        
            
                        
                    
                    
