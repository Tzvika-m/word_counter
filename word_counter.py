from flask import Flask
from flask import request
import redis
import json
import logging
from word_service import count, save_to_db, get_data_from_url, handle_file, query_word_count
from exceptions import ApiException

app = Flask(__name__)
app.debug = True
db = redis.Redis('localhost')


@app.route('/word_counter', methods=['POST'])
def count_words():
    try:
        body = request.json
        if 'text' in body:
            word_count = count(body['text'])
            save_to_db(word_count, db)
        elif 'url' in body:
            text = get_data_from_url(body['url'])
            word_count = count(text)
            save_to_db(word_count, db)
        elif 'file_path' in body:
            handle_file(body['file_path'], db)
        else:
            return 'no input', 400
    except ApiException as e:
        return e.msg, e.code
    except redis.exceptions.RedisError as e:
        logging.error('could not connect to db', e)
        return 'connection error', 500
    except Exception as e:
        logging.error('unhandled exception', e)
        return 'server error', 500

    return '', 200


@app.route('/word_counter/<word>', methods=['GET'])
def get_word_count(word):
    try:
        word_count = query_word_count(word, db)
        return json.dumps({'count': word_count}), 200
    except redis.exceptions.RedisError as e:
        logging.error('could not connect to db', e)
        return 'connection error', 500
    except Exception as e:
        logging.error('unhandled exception', e)
        return 'server error', 500


if __name__ == "__main__":
    app.run()
