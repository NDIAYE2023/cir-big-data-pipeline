from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    avg,
    stddev_pop,
    var_pop,
    sum,
    count,
    col,
)


def create_spark_session():
    """
    Create a Spark session configured with the MongoDB connector.
    """
    return (
        SparkSession.builder
        .appName("CIR_Data_Analysis")
        .config(
            "spark.jars.packages",
            "org.mongodb.spark:mongo-spark-connector_2.12:10.3.0"
        )
        .getOrCreate()
    )


def load_mongodb_collection(spark, database, collection):
    """
    Load a MongoDB collection into a PySpark DataFrame.
    """
    uri = f"mongodb://127.0.0.1/{database}.{collection}"

    return (
        spark.read
        .format("mongodb")
        .option("connection.uri", uri)
        .load()
    )


def calculate_numeric_statistics(df, column_name):
    """
    Calculate descriptive statistics for a numerical variable.
    """
    statistics = df.agg(
        avg(col(column_name)).alias("mean"),
        stddev_pop(col(column_name)).alias("standard_deviation"),
        var_pop(col(column_name)).alias("variance"),
        sum(col(column_name)).alias("total")
    )

    return statistics


def calculate_median(df, column_name):
    """
    Estimate the median using Spark's approximate quantile method.
    """
    median = df.approxQuantile(
        column_name,
        [0.5],
        0.05
    )

    return median[0] if median else None


def calculate_distribution(df, column_name):
    """
    Calculate the frequency distribution of a categorical variable.
    """
    return (
        df.groupBy(column_name)
        .agg(count("*").alias("count"))
        .orderBy(col("count").desc())
    )


def calculate_group_average(df, group_column, value_column):
    """
    Calculate the average value for each category.
    """
    return (
        df.groupBy(group_column)
        .agg(
            avg(value_column).alias("average_value"),
            count("*").alias("observations")
        )
        .orderBy(col("average_value").desc())
    )


def calculate_group_total(df, group_column, value_column):
    """
    Calculate the total value for each category.
    """
    return (
        df.groupBy(group_column)
        .agg(
            sum(value_column).alias("total_value")
        )
        .orderBy(col("total_value").desc())
    )


if __name__ == "__main__":

    spark = create_spark_session()

    # Demonstration configuration.
    # The original institutional data are not distributed.
    database = "cir_database"
    collection = "Amortissements"

    df = load_mongodb_collection(
        spark,
        database,
        collection
    )

    print("Available columns:")
    print(df.columns)

    # Example:
    # Replace "numeric_variable" with a column
    # available in the demonstration dataset.

    # stats = calculate_numeric_statistics(
    #     df,
    #     "numeric_variable"
    # )
    # stats.show()

    spark.stop()
