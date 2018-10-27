import string
import time
import sys

def scroll_text(text, delay):
    for a in text:
        print(a, end = "")
        sys.stdout.flush()
        time.sleep(delay)

skip_words = ['a', 'about', 'all', 'an', 'and', 'another', 'any', 'around','as', 'at',
              'bad', 'beautiful', 'be', 'been', 'better', 'big', 'can', 'do',  'every', 'for',
              'from', 'get', 'good', 'have', 'he', 'her', 'here', 'hers', 'his', 'how',
              'i', 'if', 'in', 'into', 'is', 'it', 'its', 'large', 'later',
              'like', 'little', 'love','may', 'main', 'me', 'mine', 'more', 'my', 'now', 'not',
              'of', 'off', 'oh', 'on', 'please', 'small', 'some', 'soon',
              'that', 'the', 'they', 'then', 'this', 'those', 'through', 'till', 'to',
              'towards', 'until', 'us', 'want', 'we', 'what', 'when', 'why',
              'wish', 'with', 'would', 'you']


def filter_words(words, skip_words):

    for x in set(words)&set(skip_words):
        words.remove(x)
    return words    

    
def remove_punct(text):

    no_punct = ""
    for char in text:
        if not (char in string.punctuation):
            no_punct = no_punct + char

    return no_punct


def normalise_input(user_input):

    no_punct = (remove_punct(user_input).lower()).strip()
    return filter_words(no_punct.split(), skip_words)
