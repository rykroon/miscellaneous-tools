import os
from random import randint
from nltk.corpus import stopwords, brown
from flask import Blueprint, request, jsonify

word_bp = Blueprint('random-words', __name__)

stopwords_set = set(stopwords.words('english'))
brown_set = set(brown.words())

diff_set = brown_set.difference(stopwords_set)
diff_set = {e.lower() for e in diff_set if e.isalpha()}

global_words = list(diff_set)

@word_bp.route('/', strict_slashes=False)
def get_random_words():
    DEFAULT_NUM_OF_WORDS = int(os.getenv('DEFAULT_NUM_OF_WORDS'))
    MAX_NUM_OF_WORDS = int(os.getenv('MAX_NUM_OF_WORDS'))
    
    word_length = int(request.args.get('word_length', 0))
    num_of_words = int(request.args.get('num_of_words', DEFAULT_NUM_OF_WORDS))
    num_of_words = min(num_of_words, MAX_NUM_OF_WORDS)
    starts_with = request.args.get('starts_with', '').lower()
    
    words = global_words

    filter_ = None
    if word_length and starts_with:
        filter_ = lambda w: len(w) == word_length and w.startswith(starts_with)
    elif word_length:
        filter_ = lambda w: len(w) == word_length
    elif starts_with:
        filter_ = lambda w: w.startswith(starts_with)
    
    if filter_:
        words = [w for w in words if filter_(w)]
    
    if len(words) < num_of_words:
        words.sort()
        return jsonify(words)

    result = set()
    while len(result) < num_of_words:
        idx = randint(0, len(words) - 1)
        result.add(words[idx])

    result = list(result)
    result.sort()
    return jsonify(result)


