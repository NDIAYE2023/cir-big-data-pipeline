from nettoyage import DataFrameCleaner
from importation import MongoDBImporter


def main():
    """
    Run the CIR data processing pipeline:
    Excel -> Cleaning -> MongoDB.
    """

    # Example path only.
    # Original institutional datasets are not included in this repository.
    file_path = "data/example_cir_data.xlsx"

    # Configuration of the different Excel sheets.
    # Column names are simplified for the public demonstration.
    file_description = {
        "file": file_path,

        "Amortissements": {
            "sheet_name": "Amortissements",
            "first_line": 4,
            "id_name": "equipment_id"
        },

        "Sous_traitance": {
            "sheet_name": "Sous-traitance",
            "first_line": 3,
            "id_name": "company_id"
        },

        "Brevets_COV": {
            "sheet_name": "Brevets & COV",
            "first_line": 3,
            "id_name": "declared_cost"
        },

        "Normalisation": {
            "sheet_name": "Normalisation",
            "first_line": 3,
            "id_name": "declared_expense"
        }
    }

    # MongoDB configuration
    mongo_uri = "mongodb://localhost:27017/"
    database_name = "cir_database"

    # Initialize data cleaner
    cleaner = DataFrameCleaner(file_path)

    # Initialize MongoDB importer
    importer = MongoDBImporter(
        mongo_uri=mongo_uri,
        db_name=database_name,
        file_description=file_description,
        cleaner=cleaner
    )

    try:
        # Process configured Excel sheets
        importer.process_sheets()

        # Process personnel data separately
        importer.process_personnel_data()

        print("CIR data pipeline completed successfully.")

    finally:
        # Always close the MongoDB connection
        importer.close_connection()


if __name__ == "__main__":
    main()
