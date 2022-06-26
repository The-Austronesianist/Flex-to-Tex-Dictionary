#Still in planning stage. Just printing things out to make sure I have the access paths correct.
#Got it so that I get everything I want. Now just need to make it write to file.

from bs4 import BeautifulSoup
import re

dictionary_file = open('configured dictionary.xhtml', 'r', encoding='utf-8')
soup = BeautifulSoup(dictionary_file, 'html.parser')

entry = soup('div')

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
                        wordclass = tag.children
                        for tag in wordclass :
                            if tag.get('class') == ['morphosyntaxanalysis'] :
                                pos_and_morphtype = tag.children
                                for tag in pos_and_morphtype :
                                    if tag.get('class') == ['partofspeech'] :
                                        pos = tag.text
                                        print(pos)
                                    if tag.get('class') == ['morphtypes'] :
                                        morphtype = tag.text
                                        print(morphtype)
                    if tag.get('class') == ['sensecontent'] :
                        sense_and_def = tag.children
                        for tag in sense_and_def :
                            if tag.get('class') == ['sensenumber'] :
                                sense_number = tag.text
                                print(sense_number)
                            if tag.get('class') == ['sense'] :
                                def_and_pos_sense = tag.children
                                for tag in def_and_pos_sense :
                                    if tag.get('class') == ['partofspeech'] :
                                        sense_pos = tag.text
                                        print(tag)
                                    if tag.get('class') == ['definitionorgloss'] :
                                        definition = tag.text
                                        print(definition)
                                    if tag.get('class') == ['examplescontents'] :
                                        examples = tag.children
                                        for tag in examples :
                                            if tag.get('class') == ['examplescontent'] :
                                                example = tag.children
                                                for tag in example :
                                                    if tag.get('class') == ['example'] :
                                                        entry_ex = tag.text
                                                        print(entry_ex)
                                                    if tag.get('class') == ['translationcontents'] :
                                                        entry_ex_trans = tag.text
                                                        print(entry_ex_trans)
