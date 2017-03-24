class DataPreprocessing:
    dummy_data = "dummy_data"

    @staticmethod
    def __run__(db):
        db.createTables()

        ##rest of the preprocessing