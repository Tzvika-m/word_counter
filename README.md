# Word Counter

Word Counter service counts words

### Prerequisites

* python 3.6 or above
* local redis running with default configurations
```
brew install redis
redis-server /usr/local/etc/redis.conf
```

### Installing and running

```
pip3 install requirements.txt
```
```
python3 word_counter.py
```

### requests examples

Text input
```
curl --header "Content-Type: application/json"   --request POST  --data '{"text": "Hi! My name is (what?), my name is (who?), my name is Slim Shady"}' http://127.0.0.1:5000/word_counter
```

URL input
```
curl --header "Content-Type: application/json"   --request POST  --data '{"url": "https://raw.githubusercontent.com/Tzvika-m/word_counter/master/test.txt"}' http://127.0.0.1:5000/word_counter
```

File input
```
curl --header "Content-Type: application/json"   --request POST  --data '{"file_path": "test.txt"}' http://127.0.0.1:5000/word_counter
```

Get a word's counter
```
curl --header "Content-Type: application/json"  http://127.0.0.1:5000/word_counter/what
```


## Authors

* **Tzvika Mordoch**
