import nltk
from nltk.tokenize import word_tokenize
class sentiAnalysis:
    def __init__(self):
        self.positiveCount=0
        self.negativeCount =0
        self.invFlag = 0
        self.invWords = ["not","lack of"]
        self.reviewText = []
    
    def computeScore(self,reviewText):
        self.reviewText = word_tokenize(reviewText)
        self.invFlag = 0
        self.positiveCount=0
        self.negativeCount =0
        for word in self.reviewText:
            if(self.invFlag == 0):
                if(self.isPositive(word)):
                    self.positiveCount = self.positiveCount +1
                elif(self.isNegative(word)):
                    self.negativeCount = self.negativeCount +1
                elif(word.lower() in self.invWords):
                    self.invFlag = 1
            else:
                if(self.isPositive(word)):
                    self.negativeCount = self.negativeCount + 1
                elif(self.isNegative(word)):
                    self.positiveCount = self.positiveCount + 1
                elif(word.lower() in self.invWords):
                    self.invFlag = 1
                self.invFlag = 0
        if(self.positiveCount + self.negativeCount > 0):
            predictedRating = (self.positiveCount/float(self.positiveCount + self.negativeCount) * 5)
            return predictedRating
        else:
            return 3
        
    def isPositive(self,word):
        lines = [line.rstrip('\n') for line in open("Positive.txt")]
        for positiveWord in lines:
            if (positiveWord==word):
                return True     
        return False

    def isNegative(self,word):
        lines = [line.rstrip('\n') for line in open("negative.txt")]
        for negativeWord in lines:
            if (negativeWord==word):
                return True     
        return False


