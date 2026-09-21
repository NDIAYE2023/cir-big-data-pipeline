from pymongo import MongoClient

from nettoyage import DataFrameCleaner


class MongoDBImporter:
    """
    Import cleaned Excel data into MongoDB collections.
    """

    def __init__(self, mongo_uri, db_name, file_description, cleaner):
        self.client = MongoClient(mongo_uri)
        self.db = self.client[db_name]
        self.file_description = file_description
        self.cleaner = cleaner

    def insert_data(self, collection_name, df):
        """
        Insert a Pandas DataFrame into a MongoDB collection.
        """
        collection = self.db[collection_name]

        records = df.to_dict("records")

        if records:
            collection.insert_many(records)

        print(
            f"'{collection_name}' successfully inserted into MongoDB."
        )

    def process_sheets(self):
        """
        Clean and import all configured Excel sheets.
        """
        for collection_name, details in self.file_description.items():

            if collection_name == "file":
                continue

            try:
                df = self.cleaner.import_and_rename(
                    sheet_name=details["sheet_name"],
                    first_line=details["first_line"],
                    id_name=details["id_name"]
                )

                self.insert_data(
                    collection_name,
                    df
                )

            except KeyError as error:
                print(
                    f"Column error in {collection_name}: {error}"
                )

            except Exception as error:
                print(
                    f"Error while importing "
                    f"'{collection_name}': {error}"
                )

    def process_personnel_data(self):
        """
        Process the personnel and young researchers dataset.
        """
        df = self.cleaner.import_personnel_data()

        df = self.cleaner.clean_dataframe(df)

        self.insert_data(
            "Personnels_et_jeunes_Docteurs",
            df
        )

    def close_connection(self):
        """
        Close the MongoDB connection.
        """
        self.client.close()
