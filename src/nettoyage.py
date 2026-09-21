import pandas as pd


class DataFrameCleaner:
    """
    Utility class for cleaning and preparing Excel data
    before database integration.
    """

    def __init__(self, file_path):
        self.file_path = file_path

    def supprimer_lignes(self, df, lignes):
        """
        Remove selected rows from a DataFrame.
        """
        return df.drop(lignes, axis=0).reset_index(drop=True)

    def clean_dataframe(self, df):
        """
        Standardize missing values and column names.
        """
        df = df.where(pd.notnull(df), None)

        df.columns = [
            str(col) if not isinstance(col, str) else col
            for col in df.columns
        ]

        return df

    def import_and_rename(self, sheet_name, first_line, id_name):
        """
        Import an Excel sheet, define its header and prepare
        the identifier column.
        """
        df = pd.read_excel(
            self.file_path,
            sheet_name=sheet_name
        )

        df = df.fillna(0)

        # Use the selected row as column names
        columns_name = list(df.iloc[first_line].values)
        df.columns = columns_name

        # Clean dataframe before database insertion
        df = self.clean_dataframe(df)

        if id_name not in df.columns:
            raise KeyError(
                f"'{id_name}' not found in columns for '{sheet_name}'"
            )

        # Convert identifier to numeric format
        df[id_name] = pd.to_numeric(
            df[id_name],
            errors="coerce"
        )

        # Remove rows without a valid identifier
        df.dropna(subset=[id_name], inplace=True)

        return df.reset_index(drop=True)

    def import_personnel_data(
        self,
        sheet_name="Personnels et jeunes Docteurs"
    ):
        """
        Import and prepare the personnel-related Excel sheet.
        """
        df = pd.read_excel(
            self.file_path,
            sheet_name=sheet_name
        )

        columns_name = list(df.iloc[4, :].values)
        df.columns = columns_name

        rows_to_remove = [
            0, 1, 2, 3, 4, 5,
            70, 71, 72, 73, 74, 75,
            76, 77, 78, 79, 80, 81,
            82, 83, 84, 85
        ]

        return self.supprimer_lignes(
            df,
            rows_to_remove
        )
