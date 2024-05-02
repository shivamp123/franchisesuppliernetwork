import os
import pymongo
import requests
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def connect_to_mongodb(database_name):
    """
    Connect to MongoDB and return the database object.

    Args:
    - database_name (str): Name of the database.

    Returns:
    - pymongo.database.Database: MongoDB database object.
    """
    try:
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        return client[database_name]
    except Exception as e:
        logger.error(f"Failed to connect to MongoDB: {e}")


def create_folder_and_save_files(folder_name, file_name, content, image_urls):
    """
    Create folder, save text file, and download images.

    Args:
    - folder_name (str): Name of the folder to be created.
    - file_name (str): Name of the text file.
    - content (str): Content to be written to the text file.
    - image_urls (list): List of image URLs to be downloaded.
    """
    try:
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

        if not os.path.exists(os.path.join(folder_name, "images")):
            os.makedirs(os.path.join(folder_name, "images"))

        with open(os.path.join(folder_name, file_name), 'w') as file:
            file.write(content)

        for image_url in image_urls:
            headers = {
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'accept-language': 'en-US,en;q=0.9,hi;q=0.8',
                'cache-control': 'max-age=0',
                'priority': 'u=0, i',
                'sec-ch-ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'document',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-site': 'none',
                'sec-fetch-user': '?1',
                'upgrade-insecure-requests': '1',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
            }
            response = requests.get(image_url,headers=headers)
            if response.status_code == 200:
                with open(os.path.join(folder_name, "images", image_url.split('/')[-1]), "wb") as f:
                    f.write(response.content)
                logger.info(f"Downloaded {image_url}")
            else:
                logger.warning("Failed to download image")

        logger.info(f"File '{file_name}' saved successfully in folder '{folder_name}'.")
    except Exception as e:
        logger.error(f"Error occurred: {e}")


def main():
    try:
        database_name = "franchi"
        db = connect_to_mongodb(database_name)
        output_db = db["output_db"]

        data_records = output_db.find()[0:2]

        for data in data_records:
            file_name = f"{data['file_name']}_{data['no']}"
            folder_path = os.path.join("D:\\p\\", file_name)
            text_content = data['des']
            image_urls = data['image']

            create_folder_and_save_files(folder_path, file_name + ".txt", text_content, image_urls)
            logger.info("Data inserted")
    except Exception as e:
        logger.error(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
