#Still in planning stage. Just printing things out to make sure I have the access paths correct. 

import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import ssl
import re

#Ignor SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

dictionary_file = open('configured dictionary.xhtml', 'r', encoding='utf-8')
soup = BeautifulSoup(dictionary_file, 'html.parser')

entry = soup('div')

#TO DO
#example sentences (look at the entry for von 'bundle')
#morpheme type (look at the entry for N-)


for div in entry :
    if div.get('class') == ['entry'] :
        span = div.children
        for tag in span :
            if tag.get('class') == ['mainheadword'] :
                headword = tag.text
                print(headword)
            if tag.get('class') == ['senses'] :
                def_and_pos = tag.children
                for tag in def_and_pos :
                    if tag.get('class') == ['sharedgrammaticalinfo'] :
                        wordclass = tag.text
                        print(wordclass)
                    if tag.get('class') == ['sensecontent'] :
                        sense_and_def = tag.children
                        for tag in sense_and_def :
                            if tag.get('class') == ['sensenumber'] :
                                sense_number = tag.text
                                print(sense_number)
                            if tag.get('class') == ['sense'] :
                                definition = tag.text
                                print(definition)
