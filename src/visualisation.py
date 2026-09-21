import matplotlib.pyplot as plt
import seaborn as sns


def plot_bar_chart(
    df,
    x_column,
    y_column,
    title="CIR Data Visualization",
    xlabel=None,
    ylabel=None
):
    """
    Create a bar chart from a Pandas DataFrame.

    Parameters
    ----------
    df : pandas.DataFrame
        Dataset containing the variables to visualize.

    x_column : str
        Column used on the x-axis.

    y_column : str
        Numerical column used on the y-axis.

    title : str
        Title of the chart.

    xlabel : str, optional
        Label of the x-axis.

    ylabel : str, optional
        Label of the y-axis.
    """

    plt.figure(figsize=(10, 6))

    sns.barplot( data=df, x=x_column, y=y_column  )

    plt.xlabel(xlabel or x_column)
    plt.ylabel(ylabel or y_column)
    plt.title(title)

    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.show()


if __name__ == "__main__":
    print(
        "Visualization module for the CIR Data Engineering Pipeline."
    )
