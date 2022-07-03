from bs4 import BeautifulSoup
import re


dictionary_file = open('configured dictionary.xhtml', 'r', encoding='utf-8')
soup = BeautifulSoup(dictionary_file, 'html.parser')

dictionary = open('dictionary.tex', 'a', encoding='utf-8')

ids = [tag['id'] for tag in soup.select('div[id]')]

def ipareplace(x) :
    return x.replace('g', '\\textipa{g}').replace('ə', '\\textipa{@}').replace('ʔ', '\\textipa{P}').replace('ŋ', '\\textipa{N}').replace('ñ', '\~n').replace('ɲ', '\\textltailn ').replace('ɨ', '\\textipa{1}').replace('ɓ', '\\textipa{\!b}').replace('ɗ', '\\textipa{\!d}').replace('ʄ', '\\textipa{\!j}').replace('ɠ', '\\textipa{\!g}')

def orthographyreplace(x) :
    return x.replace('ə', 'e').replace('ʔ', '\'').replace('ŋ', 'ng').replace('ñ', 'ny').replace('ɲ', 'ny').replace('ɨ', 'e').replace('ɓ', 'b').replace('ɗ', 'd').replace('ʄ', 'j').replace('ɠ', 'g').replace('ay', 'ai').replace('aw', 'au').replace('aia', 'aya').replace('aio', 'ayo').replace('aiu', 'ayu').replace('aie', 'aye').replace('aua', 'awa').replace('aui', 'awi').replace('aue', 'awe').replace('aua', 'awa').replace('oy', 'oi').replace('oia', 'oya').replace('oiu', 'oyu').replace('oio', 'oyo').replace('oie', 'oye')

dictionary.write(
'''\\documentclass[12pt, twoside, letterpaper, twocolumn]{article}
\\usepackage[left=1in, right=1in, top=1in, bottom=1in]{geometry}
\\usepackage{tipa}
\\usepackage{times}
\\usepackage{authblk}
\\usepackage{pdfpages}
\\usepackage{gb4e}

\\begin{document}

'''
)

for unique_id in ids :
    #Assigning all the parts to an object
    id_entry = soup.find('div', id = unique_id)

    #ALL OF THE SINGLE OCCURANCE MAIN PARENTS INSIDE ENTRY DIV

    #Contains only the head word (not universal, will create 'None')
    #complemetnary distribution with minorentrycomplex)
    mainheadword = id_entry.find(class_ = 'mainheadword')
    #Location of entry info other than head word (not universal, will create 'none')
    #complementary distribution with minorentrycomplex
    senses = id_entry.find(class_ = 'senses')
    if senses is not None :
        #I am counting how many senses there are in an entry
        sense_number = len(senses.find_all(class_ ="sensenumber"))
    #Morphologically complex forms of the head word (not universal, will create 'None')
    #not in complementary distribution (unpredictable)
    subentries = id_entry.find(class_ = 'subentries')
    if subentries is not None :
        subentry_number = len(subentries.find_all(class_ = 'subentry'))
    #Morphologically complex entries listed as a head with reference to the root entry (not universal, will create 'None')
    #complementary distribution with mainheadword and senses
    minor_headword = id_entry.find(class_ = 'headword')
    minor_reference_entry = id_entry.find(class_ = 'referencedentry')
    if minor_reference_entry is not None :
        minor_reference = minor_reference_entry.find(class_ = 'headword')

    #INSIDE SENSES
    if senses is not None :
        #sharedgrammaticalinfo only occurs if all senses have the same pos or if there is only one sense.
        #It will not be present in many entries.
        #this will create 'None' types in those cases
        sharedgrammaticalinfo = senses.find(class_ = 'sharedgrammaticalinfo')
        if sharedgrammaticalinfo is not None :
            #sharedpartofspeech only occurs if sharedgrammaticalinfo is present
            #Will create a traceback if sharedgrammaticalinfo is None
            sharedpartofspeech = sharedgrammaticalinfo.find(class_ = 'partofspeech')
            #Location of part of speech info if multiple senses with same pos

            #areas with multiple instanciations possible but not guaronteed
        else :
            #If sharedgrammaticalinfo is not present, then we have to grab multiple parts of speech.
            #I'll have to figure out how to loop through this and make sure that the proper entry gets the proper pos
            partofspeech = senses.find_all(class_ = 'partofspeech')

        #The actual definition.
        #Entries with multiple senses will have more than one.
        #Will have to figure out how to loop through it.
        if sense_number < 1:
            definitionorgloss = senses.find(class_ = 'definitionorgloss')
        if sense_number > 1 :
            definitionorgloss = senses.find_all(class_ = 'definitionorgloss')
            sensenumber = senses.find_all(class_ = 'sensenumber')

    #INSIDE SUBENTRIES

    #each subentry should have exactly one of each of these:
    if subentries is not None :
        if subentry_number < 2 :
            sub_head = subentries.find(class_ = 'headword')
            sub_pos1 = subentries.find(class_ = 'partofspeech')
            sub_pos2 = subentries.find(class_ = 'abbreviation')
            sub_def = subentries.find(class_ = 'definitionorgloss')
        if subentry_number > 1 :
            sub_head = subentries.find_all(class_ = 'headword')
            sub_senses = subentries.find_all(class_ = 'senses')


    #printing everything out once it is assigned an object.
    if mainheadword is not None :
        dictionary.write('\\noindent {\\bf ')
        dictionary.write(orthographyreplace(mainheadword.get_text().strip()))
        dictionary.write('} {\small [')
        dictionary.write(ipareplace(mainheadword.get_text().strip()))
        dictionary.write(']} ')
    if senses is not None :
        if sharedgrammaticalinfo is not None :
            dictionary.write('{\it ')
            dictionary.write(orthographyreplace(sharedpartofspeech.get_text().strip()))
            dictionary.write('} ')
            #these two if statements distinguish between entries with only one sense and entries with multiple senses.
            if sense_number < 1 :
                if definitionorgloss is not None :
                    dictionary.write(definitionorgloss.get_text().strip())
                dictionary.write('. ')
            if sense_number > 1 :
                original_sense_number = sense_number
                #this while statement is how I go through all of the senses in the list one by one.
                while sense_number > 0 :
                    dictionary.write('{\\bf ')
                    dictionary.write(sensenumber[int(original_sense_number - sense_number)].get_text().strip())
                    dictionary.write('} ')
                    dictionary.write(definitionorgloss[int(original_sense_number - sense_number)].get_text().strip())
                    dictionary.write('. ')
                    sense_number = sense_number - 1
                sense_number = original_sense_number
        else :
            original_sense_number = sense_number
            while sense_number > 0 :
                dictionary.write('{\\bf ')
                dictionary.write(sensenumber[int(original_sense_number - sense_number)].get_text().strip())
                dictionary.write('} {\it ')
                dictionary.write(partofspeech[int(original_sense_number - sense_number)].get_text().strip())
                dictionary.write('} ')
                dictionary.write(definitionorgloss[int(original_sense_number - sense_number)].get_text().strip())
                dictionary.write('. ')
                sense_number = sense_number - 1
            sense_number = original_sense_number
    if subentries is not None :
        dictionary.write('\n\n')
        if subentry_number < 2 :
            dictionary.write('{\\bf ')
            dictionary.write(orthographyreplace(sub_head.get_text().strip()))
            dictionary.write('} {\small [')
            dictionary.write(ipareplace(sub_head.get_text().strip()))
            dictionary.write(']} ')
            if sub_pos1 is not None :
                dictionary.write('{\it ')
                dictionary.write(sub_pos1.get_text().strip())
                dictionary.write('} ')
            else :
                dictionary.write('{\it ')
                dictionary.write(sub_pos2.get_text().strip())
                dictionary.write('} ')
            dictionary.write(sub_def.get_text().strip())
            dictionary.write('. ')
        if subentry_number > 1 :
            original_subentry_number = subentry_number
            while subentry_number > 0 :
                dictionary.write('{\\bf ')
                dictionary.write(orthographyreplace(sub_head[int(original_subentry_number - subentry_number)].get_text().strip()))
                dictionary.write('} {\small [')
                dictionary.write(ipareplace(sub_head[int(original_subentry_number - subentry_number)].get_text().strip()))
                dictionary.write(']} ')
                current_sub_sense = sub_senses[int(original_subentry_number - subentry_number)]
                sub_sense_number = len(current_sub_sense.find_all(class_ = 'sensenumber'))
                if current_sub_sense.find(class_ = 'sensenumber') is None :
                    dictionary.write('{\it ')
                    dictionary.write(current_sub_sense.find(class_ = 'partofspeech').get_text().strip())
                    dictionary.write('} ')
                    dictionary.write(current_sub_sense.find(class_ = 'definitionorgloss').get_text().strip())
                    dictionary.write('. ')
                elif current_sub_sense.find_all(class_ = 'sensenumber') is not None :
                    original_sub_sense_number = sub_sense_number
                    dictionary.write('{\it ')
                    dictionary.write(current_sub_sense.find(class_ = 'partofspeech').get_text().strip())
                    dictionary.write('} ')
                    while sub_sense_number > 0 :
                        current_sub_def = current_sub_sense.find_all(class_ = 'definitionorgloss')
                        dictionary.write(current_sub_def[int(original_sub_sense_number - sub_sense_number)].get_text().strip())
                        dictionary.write('. ')
                        current_sub_def = current_sub_sense.find_all(class_ = 'definitionorgloss')
                        sub_sense_number = sub_sense_number -1
                    sub_sense_number = original_sub_sense_number
                subentry_number = subentry_number - 1
                dictionary.write('\n\n')
            subentry_number = original_subentry_number
    if minor_headword is not None and mainheadword is None :
        dictionary.write('\\noindent {\\bf ')
        dictionary.write(orthographyreplace(minor_headword.get_text().strip()))
        dictionary.write('} {\small [')
        dictionary.write(ipareplace(minor_headword.get_text().strip()))
        dictionary.write(']} ')
        if minor_reference is not None :
            dictionary.write('See: ')
            dictionary.write(orthographyreplace(minor_reference.get_text().strip()))
    dictionary.write('\n\n')
dictionary.write('\end{document}')
