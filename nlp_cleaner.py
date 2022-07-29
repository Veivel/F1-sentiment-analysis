# Emoji library (for demojization)
import emoji
emojis = list(emoji.EMOJI_DATA.keys())

# Language Detection
import spacy
import spacy_fastlang # is used
from spacy_langdetect import LanguageDetector

# Stopwords to remove
from nltk.corpus import stopwords as sw
stopwords = sw.words('English')
stopwords.remove('not')

import string
import copy
import nltk
import re

class text_cleaner:
    def __init__(self):
        pass
    
    def __handle_emojis(lst):
        res = []
        for sentence in lst:
            words = sentence.split(' ')
            new_words = []
            for word in words:
                for char in word:
                    if char in emojis:
                        word.replace(char, "")
                new_words.append(word)
            sentence = ' '.join(new_words)
            res.append(sentence)
        return res
            

    def __clean_sentences(lst):
        ''' Cleans up a list of tweets.
        Removes: Links, tags, retweets, emojis'''
        
        res = []
        for sentence in lst:
            sentence = sentence.lower()     # lower-cases sentence
            
            words = sentence.split(' ')
            new_words = copy.deepcopy(words)
            
            for word in words: # Iterates through each word in the tweet
                if len(word) == 0:
                    new_words.remove(word)
                elif word[:4] == "http":    # Removes links
                    new_words.remove(word)
                elif word[0] == "@":        # Removes tags
                    new_words.remove(word)
                elif word in stopwords:     # Removes stopwords
                    new_words.remove(word)
                elif word[:2] == "rt":      # Removes retweets
                    new_words.remove(word)
                elif word[:2] == "\n":      # Removes line breaks
                    new_words.remove(word)
                                            
            sentence = " ".join(new_words)
            # sentence = re.sub(string.punctuation, '', sentence) # Removes punctuation
            for chr in string.punctuation:
                sentence = sentence.replace(chr, "")
            
            res.append(sentence)
        return res

    def __clean_words(lst):
        ''' Removes: empty spaces'''
        res = []
        for sentence in lst:
            words = sentence.split(' ')
            new_words = []
            
            for word in words:
                for char in word: # iterates through each character in the tweet
                    if char == " ":
                        word.replace(char, "")
                new_words.append(word)
                
            sentence = " ".join(new_words)
            res.append(sentence) 
        return res
        
    def remove_non_english(lst):
        ''' Removes all content that is NOT english from a list of tweets'''
        langs = []
        res = copy.deepcopy(lst)
        
        nlp = spacy.load("en_core_web_sm")
        nlp.add_pipe("language_detector")
        
        for item in lst: # iterates through each sentence
            doc = nlp(item)
            lang = doc._.language
            if lang != 'en':
                res.remove(item)        # removes non-english sentences
            langs.append(lang)
        # lang_labels['language'] = langs # secondary side-effect
        return res

    def __stem(lst):
        '''Stems words to use basic stem word (e.g turn instead of turning)'''
        ps = nltk.stem.PorterStemmer()
        res = []
        for sentence in lst:
            new_sentence = []
            for word in sentence.split():
                new_word = ps.stem(word)
                new_sentence.append(new_word)
            new_sentence = " ".join(new_sentence)
            res.append(new_sentence)
        return res
    
    def clean(df):
        ''' Static method to do cleaning'''
        
        df = text_cleaner.__handle_emojis(df)
        df = text_cleaner.__clean_sentences(df)
        # df = text_cleaner.remove_non_english(df)
        df = text_cleaner.__stem(df)
        return df