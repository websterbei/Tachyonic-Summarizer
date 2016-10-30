from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals

from sumy.parsers.html import HtmlParser
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words


LANGUAGE = "english"
SENTENCES_COUNT = 5


import logging
import requests

from flask import Flask, render_template

from flask_ask import Ask, statement, question, session


app = Flask(__name__)

ask = Ask(app, "/")

logging.getLogger("flask_ask").setLevel(logging.DEBUG)

url = "https://c71251c1.ngrok.io/"
@ask.launch
def new_game():

    welcome_msg = render_template('welcome')

    return question(welcome_msg)


@ask.intent("Start",convert={'first':int,'second':int,'third':int})
def startRecording(first,second,third): 
    msg = render_template('start')
    response = requests.get(url+"msg?cmd=start"+"&fname="+str(first)+str(second)+str(third))
    return statement(str(first)+str(second)+str(third))


@ask.intent("End")
def endRecording():
    msg = render_template('end')
    response = requests.get(url+"msg?cmd=end")
    return statement(msg)

@ask.intent("Play",convert={'first':int,'second':int,'third':int})
def readSum(first,second,third):
    #response = requests.get(url+"play?fname="+str(first)+str(second)+str(third))
    parser = HtmlParser.from_url(url+"play?fname="+str(first)+str(second)+str(third), Tokenizer(LANGUAGE))
    stemmer = Stemmer(LANGUAGE)
    summarizer = Summarizer(stemmer)
    summarizer.stop_words = get_stop_words(LANGUAGE)
    msg = ""
    for sentence in summarizer(parser.document, SENTENCES_COUNT):    
        msg = msg + sentence.__str__()
    return statement(msg)

if __name__ == '__main__':
    app.run(debug=True)
