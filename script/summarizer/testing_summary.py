from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals

from sumy.parsers.html import HtmlParser
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words
LANGUAGE = "english"
import os

# SENTENCES_COUNT = 3


def get_summary(text_lst,SENTENCES_COUNT):
    # url = "http://www.zsstritezuct.estranky.cz/clanky/predmety/cteni/jak-naucit-dite-spravne-cist.html"
    # parser = HtmlParser.from_url(url, Tokenizer(LANGUAGE))
    # or for plain text files
    for text_file in text_lst:
        parser = PlaintextParser.from_file(text_file, Tokenizer(LANGUAGE))
        stemmer = Stemmer(LANGUAGE)

        summarizer = Summarizer(stemmer)
        summarizer.stop_words = get_stop_words(LANGUAGE)

        sentence_lst=[]
        with open(text_file.replace('_text.csv', '_summary.csv'), 'a') as file:
            for sentence in summarizer(parser.document, SENTENCES_COUNT):
                sentence_lst.append(sentence)
                file.write(str(sentence))
                file.write(' ')
#
# if __name__=='__main__':
#     txt_lst=[]
#     for root,dirs,files in os.walk(r'D:\latest_version\IntermediateVideoText'):
#         for f in files:
#             if f.endswith('_text.csv') and not f.endswith('_audio_text.csv'):
#                 txt_lst.append(root+'\\'+f)
#     get_summary(txt_lst,2)