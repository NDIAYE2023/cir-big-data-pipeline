import pandas as pd


def lire_excel(file_path, sheet_name):
    """
    Read a specific sheet from an Excel file.

    Parameters
    ----------
    file_path : str
        Path to the Excel file.
    sheet_name : str
        Name of the Excel sheet.

    Returns
    -------
    pandas.DataFrame
        Data contained in the selected sheet.
    """
    return pd.read_excel(file_path, sheet_name=sheet_name)
