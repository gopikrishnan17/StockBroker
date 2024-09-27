import os, glob
import csv
from datetime import date, timedelta
from jugaad_data.nse import bhavcopy_save

def download_bhavcopy():
    # Start from today and move back one day at a time if no valid response
    current_date = date.today()
    directory = "bhavcopy_dir"
    os.makedirs(directory, exist_ok=True)
    for file in glob.glob(directory+'/*'):
        os.remove(file)

    while True:
        try:
            # Try downloading the bhavcopy for the current date
            bhavcopy_save(current_date, directory)

        except Exception as e:
            print(f"No bhavcopy available for {current_date}: {e}")
        else:
            break
        
        # Move back one day
        current_date -= timedelta(days=1)

    return directory

def process_bhavcopy(directory):
    txt_filename = "nse_symbols_full.txt"

    # Open the CSV file inside the ZIP and process it
    file = os.listdir(directory)[0]
    file = directory + '/' + file
    with open(file, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)

        # Write to the text file
        with open(txt_filename, 'w') as txt_file:
            for row in csv_reader:
                if row["SERIES"] == "EQ":
                    txt_file.write(row["SYMBOL"] + '\n')

    # Delete the CSV file after processing
    for file in glob.glob(directory+'/*'):
        os.remove(file)
    print(f"{txt_filename} created successfully. CSV file deleted.")

if __name__ == "__main__":
    csv_filename = download_bhavcopy()
    process_bhavcopy(csv_filename)
