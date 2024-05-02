# Web Scraping and MongoDB Data Insertion

This Python script scrapes data from a list of URLs, processes the scraped content, and inserts it into a MongoDB database.

## Prerequisites

Before running the script, ensure you have the following installed:

- Python 3.x
- pymongo
- requests
- scrapy

## Installation

1. Clone the repository:

git clone <repository_url>


2. Install dependencies:

pip install pymongo requests scrapy


## Usage

1. Modify the MongoDB connection string in the script to match your MongoDB server configuration.

2. Ensure that MongoDB is running.

3. Run the script:

python main.py


## Functionality

- **get_response(url)**: Sends a GET request to the provided URL, extracts the response, and returns an HtmlResponse object.

- **extract_data_from_urls(url_list)**: Scrapes data from a list of URLs, processes the scraped content, and inserts it into a MongoDB database.

## Main Code

The script starts by fetching a sitemap index XML file from the website "franchisesuppliernetwork.com". It then extracts URLs from the sitemap index and further processes each URL to extract relevant data. The extracted data includes file names, titles, details, descriptions, URLs, images, and reference URLs. Finally, the data is inserted into a MongoDB database.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.


==========================================================================================================================================================================================================


# Folder and File Creator

This Python script connects to a MongoDB database, retrieves data records, creates a folder, saves a text file with content, and downloads images from URLs.

## Prerequisites

Before running the script, ensure you have the following installed:

- Python 3.x
- pymongo
- requests

## Installation

1. Clone the repository:

git clone <repository_url>

2. Install dependencies:

pip install pymongo requests


## Usage

1. Modify the MongoDB connection string in the `connect_to_mongodb` function to match your MongoDB server configuration.

2. Ensure that MongoDB is running.

3. Run the script:

python downlaod_file.py


## Functionality

- **connect_to_mongodb(database_name)**: Connects to MongoDB and returns the database object.

- **create_folder_and_save_files(folder_name, file_name, content, image_urls)**: Creates a folder, saves a text file with content, and downloads images from URLs.

- **main()**: Main function that retrieves data records from MongoDB, creates folders, saves text files, and downloads images.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.


