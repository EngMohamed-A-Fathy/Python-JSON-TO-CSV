# Python-JSON-TO-CSV
## Introduction 

In 2012, Bitly, a popular URL shortening service, collaborated with the US government website USA.gov to collect anonymous data from users who shortened links ending with ".gov" or ".mil". This data was made available in the form of a text file in JSON format.

The JSON file contains various keys and their respective descriptions. For this task, only the most important keys will be utilized.

## Aim
This is a Python script that converts JSON files into CSV format. The script reads JSON files from a source directory, extracts the relevant information, and outputs it to CSV files in a target directory.

## Steps
### The script performs the following transformations on the data:

Extracts only the columns we need from the input JSON files
Renames the columns to a more readable format
Splits the user_agent column into web_browser and operating_sys columns
Extracts the operating system from the operating_sys column
Extracts the domain from the from_url and to_url columns
Splits the longitude_latitude column into latitude and longitude columns
Rounds the latitude and longitude columns to 2 decimal places
Removes any rows with missing data in the city, longitude, or latitude columns
Getting Started
To use this script, follow these steps:

Install Python 3 on your computer if you haven't already done so.
Download the script file json_csv_convertor.py from the repository and save it to your desired location.
Open a terminal or command prompt and navigate to the directory where the script is located.

## Runing of script
Run the script using the following command:
php

#### python json_csv_convertor.py <source_dir> <target_dir> <unix_time>
#### <source_dir> is the path to the directory containing the JSON files you want to convert.
#### <target_dir> is the path to the directory where you want to save the CSV files (optional - if not provided, the CSV files will be saved to the source directory).
#### <unix_time> is an optional flag that specifies whether to output time in Unix format or human-readable format (default is human-readable format).

### Example usage:

bash
python json_csv_convertor.py /path/to/json/files /path/to/csv/files yes
This will convert all JSON files in the /path/to/json/files directory to CSV files and save them in the /path/to/csv/files directory, with timestamps in Unix format.

## Dependencies
This script requires the following Python packages to be installed:

pandas
numpy
You can install these packages using pip:

#### pip install pandas numpy

Notes
The script assumes that the JSON files are in the following format:
css
Copy code
{
    "a": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    "r": "https://www.google.com/",
    "u": "https://example.com/",
    "cy": "New York",
    "ll": [
        40.7128,
        -74.006
    ],
    "tz": "America/New_York",
    "t": 1493908516,
    "hc": 1493908532
}
The script will only process files with the .json extension in the source directory.
The output CSV files will have the same name as the input JSON files, with the .csv extension instead.
If there are any errors in processing a file, the script will skip that file and continue with the rest. A message will be printed to the console indicating which file was skipped.
The script may take some time to run, especially if there are many large JSON files in the source directory.
