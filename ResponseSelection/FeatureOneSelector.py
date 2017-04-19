from ResponseSelection.ResponseSelector import ResponseSelector
from NLP.TextParser import TextParser


class FeatureOneSelector(ResponseSelector):
    def getAnswer(self, question):
        tokens = TextParser.tokenize(question)
        filtered_tokens = TextParser.extractKeywords(tokens)
        return {
            "speech": str(filtered_tokens),
            "displayText": "",
            "data": {},
            "contextOut": [],
            "source": "prof-3abqarino"
        }
