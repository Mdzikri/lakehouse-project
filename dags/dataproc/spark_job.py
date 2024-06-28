from pyspark.sql import SparkSession

def main():
    spark = SparkSession.builder.appName('GCS to Parquet').getOrCreate()

    # Membaca data dari GCS
    df = spark.read.csv('gs://testing-de/data/exported_data.csv', header=True)

    # Lakukan beberapa pemrosesan data
    #df_filtered = df.filter(df['some_column'] > 0)

    # Menyimpan hasil ke GCS sebagai file Parquet
    df.write.parquet('gs://testing-de/data/output_data.parquet', mode='overwrite')

    spark.stop()

if __name__ == "__main__":
    main()

