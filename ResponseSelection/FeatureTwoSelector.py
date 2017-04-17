from ResponseSelection.ResponseSelector import ResponseSelector
from Data import DataAccess

class FeatureTwoSelector:
    
    def getRandomQuestion(self):
        row = DataAccess.DataAccess().getRandomQuestion()
        print "------------" + row[0][0] + "---------"

