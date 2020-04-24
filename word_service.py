from collections import Counter
import requests
import logging
from exceptions import ApiException

DELIMITERS = ['!', '?', '(', ')', ',', '.', ';', ':', '-', '_', '*', '"', "'", '/', '\\']
LINE_NUM_BUFFER = 10


def split(string, delimiters):
    for delim in delimiters:
        string = string.replace(delim, ' ')
    return string.split()


def count(string):
    words = split(string.lower(), DELIMITERS)
    return Counter(words)


def save_to_db(word_count, db):
    for word in word_count:
        db.incrby(word, word_count[word])


def get_data_from_url(url):
    try:
        response = requests.get(url)
        if response.status_code != 200:
            raise ApiException('url returned bad response', 400)
        else:
            return str(response.content)
    except requests.exceptions.RequestException as e:
        logging.error('error connecting to input url', e)
        raise ApiException('error while requesting url', 500)


def handle_file(path, db):
    line_number = 1
    accumulative_count = Counter()
    try:
        with open(path, 'r') as reader:
            line = reader.readline()
            while line != '':  # The EOF char is an empty string
                line_word_count = count(line)
                accumulative_count += line_word_count

                # If we reached the buffer size, save to the DB and clear the counters
                if line_number == LINE_NUM_BUFFER:
                    save_to_db(accumulative_count, db)
                    accumulative_count = Counter()
                    line_number = 0

                line = reader.readline()
                line_number += 1

            # Save the remaining lines to the DB
            save_to_db(accumulative_count, db)
    except FileNotFoundError:
        raise ApiException('file not found', 400)
    except OSError as e:
        logging.error('error in file handling', e)
        raise ApiException('error in file handling', 500)
