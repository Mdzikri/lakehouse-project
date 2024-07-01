from pyspark.sql import SparkSession
from pyspark.sql.functions import avg, count, col
import logging

def main():
    # Set up logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger('Gaming Data Aggregation')

    spark = SparkSession.builder.appName('Gaming Data Aggregation').getOrCreate()

    try:
        # Membaca data dari GCS
        logger.info("Membaca data dari GCS")
        df = spark.read.csv('gs://testing-de/data/data-source.csv', header=True, inferSchema=True)
        logger.info("Data berhasil dibaca")

        # Agregasi 1: Jumlah pengguna unik per negara
        logger.info("Melakukan agregasi jumlah pengguna unik per negara")
        df_country_users = df.groupBy('Location').agg(count('PlayerID').alias('unique_users'))
        logger.info("Agregasi 1 selesai")

        # Agregasi 2: Rata-rata total waktu bermain per genre
        logger.info("Melakukan agregasi rata-rata total waktu bermain per genre")
        df_genre_avg_time = df.groupBy('GameGenre').agg(avg('PlayTimeHours').alias('avg_play_time'))
        logger.info("Agregasi 2 selesai")

        # Menyimpan hasil ke GCS sebagai file Parquet
        logger.info("Menyimpan hasil agregasi ke GCS")
        df_country_users.write.parquet('gs://testing-de/datahub/country_users.parquet', mode='overwrite')
        df_genre_avg_time.write.parquet('gs://testing-de/datahub/genre_avg_time.parquet', mode='overwrite')
        logger.info("Data berhasil disimpan ke GCS")
    
    except Exception as e:
        logger.error("Error saat menjalankan script", exc_info=True)
    
    finally:
        spark.stop()
        logger.info("Spark session stopped")

if __name__ == "__main__":
    main()
