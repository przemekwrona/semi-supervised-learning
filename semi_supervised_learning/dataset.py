import zipfile
import gzip
import shutil
import requests
import os

COVER_TYPE_URL = "https://www.openml.org/data/download/2418/covtype-normalized.arff"
COVER_TYPE_ZIP = "resources/covertype.zip"
COVER_TYPE_DEST = "resources/covertype"
COVER_TYPE_GZ = "{}/covtype.data.gz".format(COVER_TYPE_DEST)
COVER_TYPE_DECOMPRESSED = "{}/{}".format(COVER_TYPE_DEST, "covtype.data")
COVER_TYPE_ARFF = "{}/{}".format(COVER_TYPE_DEST, "covtype.arff")


def unzip_file(zip_filepath, extract_to_dir):
    """
    Unzips a specified zip file to a target directory.

    Args:
        zip_filepath (str): The path to the zip file.
        extract_to_dir (str): The directory where contents will be extracted.
    """
    if not os.path.exists(extract_to_dir):
        os.makedirs(extract_to_dir)

    try:
        with zipfile.ZipFile(zip_filepath, 'r') as zip_ref:
            zip_ref.extractall(extract_to_dir)
        print(f"Successfully unzipped '{zip_filepath}' to '{extract_to_dir}'")
    except zipfile.BadZipFile:
        print(f"Error: '{zip_filepath}' is not a valid zip file or is corrupted.")
    except Exception as e:
        print(f"An error occurred: {e}")


def decompress_gz(gz_filepath, output_filepath):
    """
    Decompresses a .gz file to a specified output file.

    Args:
        gz_filepath (str): The path to the .gz file.
        output_filepath (str): The path where the decompressed file will be saved.
    """
    print(gz_filepath)
    try:
        with gzip.open(gz_filepath, 'rb') as f_in:
            with open(output_filepath, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        print(f"Successfully decompressed '{gz_filepath}' to '{output_filepath}'")
    except FileNotFoundError:
        print(f"Error: The file '{gz_filepath}' was not found.")
    except gzip.BadGzipFile:
        print(f"Error: '{gz_filepath}' is not a valid gzip file or is corrupted.")
    except Exception as e:
        print(f"An error occurred: {e}")


def convert_data_to_arff(data_filepath, arff_filepath, relation_name, attribute_definitions, skip_header=False):
    """
    Converts a .data file to an ARFF file.

    Args:
        data_filepath (str): Path to the input .data file.
        arff_filepath (str): Path to the output .arff file.
        relation_name (str): The name for the ARFF relation (e.g., 'IrisDataset').
        attribute_definitions (list): A list of tuples, where each tuple is
                                      (attribute_name, attribute_type_or_values).
                                      For example: ('sepal_length', 'numeric'),
                                                   ('species', '{Iris-setosa,Iris-versicolor,Iris-virginica}')
        skip_header (bool): Set to True if the .data file has a header row that should be skipped.
    """
    try:
        with open(data_filepath, 'r') as infile:
            lines = infile.readlines()

        if skip_header and lines:
            lines = lines[1:]  # Skip the first line if it's a header

        with open(arff_filepath, 'w') as outfile:
            # Write ARFF header
            outfile.write(f"@relation {relation_name}\n\n")

            for name, definition in attribute_definitions:
                outfile.write(f"@attribute {name} {definition}\n")
            outfile.write("\n@data\n")

            # Write data
            for line in lines:
                # Remove leading/trailing whitespace and write to ARFF
                # Assuming comma-separated values in .data file
                # You might need to adjust this depending on your .data file's delimiter
                cleaned_line = line.strip()
                if cleaned_line:  # Ensure line is not empty
                    outfile.write(cleaned_line + "\n")

        print(f"Successfully converted '{data_filepath}' to '{arff_filepath}'")

    except FileNotFoundError:
        print(f"Error: Input file '{data_filepath}' not found.")
    except Exception as e:
        print(f"An error occurred during conversion: {e}")


def download_file_basic(url, local_filename):
    """
    Downloads a file from a URL to a local path.
    Suitable for smaller files as it loads the entire content into memory.

    Args:
        url (str): The URL of the file to download.
        local_filename (str): The path to save the downloaded file.
    """
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)

        with open(local_filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"Successfully downloaded '{local_filename}' from '{url}'")
        return True
    except requests.exceptions.RequestException as e:
        print(f"Error downloading '{url}': {e}")
        return False
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False


def ensure_directory_exists(directory_path):
    """
    Checks if a directory exists and creates it if it doesn't.
    Handles creation of parent directories if they don't exist.

    Args:
        directory_path (str): The path to the directory to check/create.
    """
    try:
        os.makedirs(directory_path, exist_ok=True)
        print(f"Directory '{directory_path}' ensured to exist.")
    except OSError as e:
        print(f"Error creating directory '{directory_path}': {e}")


def download_cover_type():
    ensure_directory_exists(COVER_TYPE_DEST)
    if not os.path.exists("{}/covettype.arff".format(COVER_TYPE_DEST)):
        print(f"Download Cover Type dataset ...")
        download_file_basic(COVER_TYPE_URL, "{}/covettype.arff".format(COVER_TYPE_DEST))

    print(f"Cover Type dataset has been already downloaded")
