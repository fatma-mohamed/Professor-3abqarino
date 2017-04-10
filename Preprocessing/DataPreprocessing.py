from Data import Database

class DataPreprocessing:

    @staticmethod
    def __run__(db):
        db.createTables()

        ##rest of the preprocessing