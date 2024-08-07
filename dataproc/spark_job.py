from pyspark.sql import SparkSession
from pyspark.sql.functions import sum as _sum
import matplotlib.pyplot as plt
import pandas as pd
import logging
from google.cloud import storage

def upload_to_gcs(local_file_path, bucket_name, gcs_file_path):
    client = storage.Client()
    bucket = client.get_bucket(bucket_name)
    blob = bucket.blob(gcs_file_path)
    blob.upload_from_filename(local_file_path)

def main():
    # Set up logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger('Gaming Data Aggregation')

    spark = SparkSession.builder.appName('Gaming Data Aggregation').getOrCreate()

    try:
        # Membaca data dari GCS
        logger.info("Membaca data dari GCS")
        df = spark.read.csv('gs://testing-de/testing/real.csv', header=True, inferSchema=True)
        logger.info("Data berhasil dibaca")

        # Agregasi: Total PlayTimeHours dan AchievementsUnlocked berdasarkan Gender dan GameDifficulty
        logger.info("Melakukan agregasi total PlayTimeHours dan AchievementsUnlocked berdasarkan Gender dan GameDifficulty")
        df_aggregated = df.groupBy('Gender', 'GameDifficulty').agg(
            _sum('PlayTimeHours').alias('TotalPlayTimeHours'),
            _sum('AchievementsUnlocked').alias('TotalAchievementsUnlocked')
        ).toPandas()
        logger.info("Agregasi selesai")

        # Visualisasi menggunakan matplotlib
        logger.info("Membuat visualisasi")
        fig, ax = plt.subplots(2, 1, figsize=(12, 12))

        # Bar plot untuk Total PlayTimeHours
        playtime_plot = df_aggregated.pivot(index='GameDifficulty', columns='Gender', values='TotalPlayTimeHours')
        playtime_plot.plot(kind='bar', ax=ax[0], rot=0)
        ax[0].set_title('Total Play Time Hours by Gender and Game Difficulty')
        ax[0].set_ylabel('Total Play Time Hours')

        # Bar plot untuk Total AchievementsUnlocked
        achievements_plot = df_aggregated.pivot(index='GameDifficulty', columns='Gender', values='TotalAchievementsUnlocked')
        achievements_plot.plot(kind='bar', ax=ax[1], rot=0)
        ax[1].set_title('Total Achievements Unlocked by Gender and Game Difficulty')
        ax[1].set_ylabel('Total Achievements Unlocked')

        plt.tight_layout()
        local_file_path = '/tmp/gaming_data_visualization.png'
        plt.savefig(local_file_path)
        logger.info("Visualisasi selesai dan disimpan sebagai gambar")

        # Upload gambar ke GCS
        logger.info("Mengunggah gambar ke GCS")
        upload_to_gcs(local_file_path, 'testing-de', 'data/visualizations/gaming_data_visualization.png')
        logger.info("Gambar berhasil diunggah ke GCS")

    except Exception as e:
        logger.error("Error saat menjalankan script", exc_info=True)
    
    finally:
        spark.stop()
        logger.info("Spark session stopped")

if __name__ == "__main__":
    main()
