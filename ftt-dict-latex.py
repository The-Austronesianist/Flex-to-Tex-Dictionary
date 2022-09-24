from bs4 import BeautifulSoup
import re

#Take the FLEx configured dictionary XHTML export file and convert it to a latex
#(and txt) file for compiling as a proper dictionary. I am basically going
#through each div entry, grabbing the html for that entry, then rearranging
#everything within to how I want it to appear in the LaTeX.

#1  loop through the id tags in a for loop
    #example: <div class="entry" id="g4dea436c-ff5b-470a-bb82-34c88e14c3a9">
    #assign each unique entry id to unique_id

#2  for each unique_id, go through and grab what I want from the HTML

#3  rearrange everything how I want it to appear in the LaTeX



dictionary_file = open('dictionary.xhtml', 'r', encoding='utf-8')
soup = BeautifulSoup(dictionary_file, 'html.parser')

dictionary = open('dictionary.tex', 'a', encoding='utf-8')
dictionary_txt = open('dictionary.txt', 'a', encoding='utf-8')

#I create a list of id identifiers and the associated html. I did it this way,
#instead of running through each div in order, because i was getting some wierd
#errors. This has the unfortunate consequence of making it impossible for me to
#automate newpaging and giving titles to letter sections, because the html for
#a A, b B, etc, does not have an id tag.
ids = [tag['id'] for tag in soup.select('div[id]')]

def ipareplace(x) :
    #replaces the IPA with textipa format for LaTeX
    return x.replace('1', '').replace('2', '').replace('3', '').replace('4', '').replace('5', '').replace('g', '\\textipa{g}').replace('ə', '\\textipa{@}').replace('ʔ', '\\textipa{P}').replace('ŋ', '\\textipa{N}').replace('ñ', '\~n').replace('ɲ', '\\textltailn ').replace('ɨ', '\\textipa{1}').replace('ɓ', '\\textipa{\!b}').replace('ɗ', '\\textipa{\!d}').replace('ʄ', '\\textipa{\!j}').replace('ɠ', '\\textipa{\!g}')

def orthographyreplace(x) :
    #replaces the IPA with the orthography
    return x.replace('ə', 'e').replace('ʔ', '\'').replace('ŋ', 'ng').replace('ñ', 'ny').replace('ɲ', 'ny').replace('ɨ', 'e').replace('ɓ', 'b').replace('ɗ', 'd').replace('ʄ', 'j').replace('ɠ', 'g').replace('ay', 'ai').replace('aw', 'au').replace('aia', 'aya').replace('aio', 'ayo').replace('aiu', 'ayu').replace('aie', 'aye').replace('aua', 'awa').replace('aui', 'awi').replace('aue', 'awe').replace('aua', 'awa').replace('oy', 'oi').replace('oia', 'oya').replace('oiu', 'oyu').replace('oio', 'oyo').replace('oie', 'oye').replace('1', '\\textsubscript{1}').replace('2', '\\textsubscript{2}').replace('3', '\\textsubscript{3}').replace('4', '\\textsubscript{4}').replace('5', '\\textsubscript{5}')

#Write prenamble stuff for the LaTeX file
dictionary.write(
'''\\documentclass[12pt, twoside, letterpaper, twocolumn]{article}
\\usepackage[left=1in, right=1in, top=1in, bottom=1in]{geometry}
\\usepackage{changepage}
\\usepackage{tipa}
\\usepackage[hidelinks]{hyperref}
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

    #Contains only the head word
    mainheadword = id_entry.find(class_ = 'mainheadword')
    #Location of entry info other than head word
    senses = id_entry.find(class_ = 'senses')
    if senses is not None :
        #I am counting how many senses there are in an entry
        sense_number = len(senses.find_all(class_ ="sensenumber"))
    #Morphologically complex forms of the head word (not universal, will create 'None')
    subentries = id_entry.find(class_ = 'subentries')
    if subentries is not None :
        subentry_number = len(subentries.find_all(class_ = 'subentry'))
    #Morphologically complex entries listed as a head with reference to the root entry (not universal, will create 'None')
    minor_headword = id_entry.find(class_ = 'headword')
    minor_reference_entry = id_entry.find(class_ = 'referencedentry')
    if minor_reference_entry is not None :
        minor_reference = minor_reference_entry.find(class_ = 'headword')
        main_reference = minor_reference.find(href = True)
        main_reference  = main_reference['href']
    minor_type = id_entry.find(class_ = 'reverseabbr')
    borrowing = id_entry.find(class_ = 'etymologies')

    #INSIDE SENSES
    if senses is not None :
        #sharedgrammaticalinfo only occurs if all senses have the same pos or if there is only one sense.
        sharedgrammaticalinfo = senses.find(class_ = 'sharedgrammaticalinfo')
        if sharedgrammaticalinfo is not None :
            #sharedpartofspeech only occurs if sharedgrammaticalinfo is present
            sharedpartofspeech = sharedgrammaticalinfo.find(class_ = 'partofspeech')
            #Location of part of speech info if multiple senses with same pos
        else :
            #If sharedgrammaticalinfo is not present, then we have to grab multiple parts of speech.
            partofspeech = senses.find_all(class_ = 'partofspeech')

        #The actual definition.
        if sense_number < 1:
            definitionorgloss = senses.find(class_ = 'definitionorgloss')
            scientificname = senses.find(class_ = 'scientificname')
            anthronote = senses.find(class_ = 'anthronote')
            socio_note = senses.find(class_ = 'sociolinguisticsnote')
            examplescontent_number = len(senses.find_all(class_ = 'examplescontent'))
            if examplescontent_number > 0 :
                if examplescontent_number == 1 :
                    example = senses.find(class_ = 'example')
                    translation = senses.find(class_ = 'translation')
                if examplescontent_number > 1 :
                    example = senses.find_all(class_ = 'example')
                    translation = senses.find_all(class_ = 'translation')
        if sense_number > 1 :
            definitionorgloss = senses.find_all(class_ = 'definitionorgloss')
            sensenumber = senses.find_all(class_ = 'sensenumber')
            sensecontent = senses.find_all(class_ = 'sensecontent')

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
    #there's alot of stuff in here that is just meant to make the LaTeX look
    #nice, like all the new lines and tabs and what not.
    if mainheadword is not None :
        dictionary.write('\\vspace{6pt} \n')
        dictionary.write('\hypertarget{')
        dictionary.write(unique_id)
        dictionary.write('} \n')
        dictionary.write('\\noindent {\\large \\bf ')
        dictionary.write(orthographyreplace(mainheadword.get_text().strip()))
        dictionary_txt.write(orthographyreplace(mainheadword.get_text().strip()))
        dictionary.write('} \n{\\small [')
        dictionary.write(ipareplace(mainheadword.get_text().strip()))
        dictionary_txt.write('\t [')
        dictionary_txt.write(mainheadword.get_text().strip())
        dictionary_txt.write('] \t')
        dictionary.write(']} \n')
    if borrowing is not None :
        dictionary.write('{\\small ({\\sc \\lowercase{')
        dictionary.write(borrowing.find(class_ = 'language').get_text().strip())
        dictionary.write('}}: ')
        dictionary.write(borrowing.find(class_ = 'form').get_text().strip())
        dictionary.write(')} \n')
    if senses is not None :
        if sharedgrammaticalinfo is not None :
            dictionary.write('{\\it \\normalsize ')
            dictionary.write(orthographyreplace(sharedpartofspeech.get_text().strip()))
            dictionary.write('} \n')
            #these two if statements distinguish between entries with only one sense and entries with multiple senses.
            if sense_number < 1 :
                if definitionorgloss is not None :
                    dictionary.write('{\\normalsize ')
                    dictionary.write(definitionorgloss.get_text().strip())
                    dictionary_txt.write(definitionorgloss.get_text().strip())
                    dictionary_txt.write('\t')
                    dictionary.write('} \n')
                    if scientificname is not None :
                        dictionary.write('{ \\normalsize ({\\it ')
                        dictionary.write(scientificname.get_text().strip())
                        dictionary.write('}).} \n')
                    if anthronote is not None :
                        dictionary.write(' {\\normalsize {\\it Cultural note: }')
                        dictionary.write(anthronote.get_text().strip())
                        dictionary.write('} \n')
                    if socio_note is not None :
                        dictionary.write(' {\\normalsize {\\it Social note: }')
                        dictionary.write(socio_note.get_text().strip())
                        dictionary.write('} \n')
                if examplescontent_number > 0 :
                    if examplescontent_number == 1 :
                        dictionary.write('{\\small \\sc example:} { \\normalsize \\it ')
                        dictionary.write(orthographyreplace(example.get_text().strip()))
                        dictionary.write('} \n{\\small [')
                        dictionary.write(ipareplace(example.get_text().strip())[:-1])
                        dictionary.write(']} \n{\\normalsize `')
                        dictionary.write(translation.get_text().strip())
                        dictionary.write('\'} \n')
                    if examplescontent_number > 1 :
                        examplescontent_number_original = examplescontent_number
                        while examplescontent_number > 0 :
                            dictionary.write('{\\small \\sc example:} {\\normalsize \\it ')
                            dictionary.write(orthographyreplace(example[int(examplescontent_number_original - examplescontent_number)].get_text().strip()))
                            dictionary.write('} \n{\\small [')
                            dictionary.write(ipareplace(example[int(examplescontent_number_original - examplescontent_number)].get_text().strip())[:-1])
                            dictionary.write(']} \n{\\normalsize`')
                            dictionary.write(translation[int(examplescontent_number_original - examplescontent_number)].get_text().strip())
                            dictionary.write('\'} \n')
                            examplescontent_number = examplescontent_number - 1
            if sense_number > 1 :
                original_sense_number = sense_number
                #this while statement is how I go through all of the senses in the list one by one.
                while sense_number > 0 :
                    dictionary.write('{\\normalsize {\\bf ')
                    dictionary.write(sensenumber[int(original_sense_number - sense_number)].get_text().strip())
                    dictionary.write('} ')
                    dictionary_txt.write(sensenumber[int(original_sense_number - sense_number)].get_text().strip())
                    dictionary_txt.write('\t')
                    dictionary.write(definitionorgloss[int(original_sense_number - sense_number)].get_text().strip())
                    dictionary.write('} \n')
                    dictionary_txt.write(definitionorgloss[int(original_sense_number - sense_number)].get_text().strip())
                    dictionary_txt.write('\t')
                    if sensecontent[int(original_sense_number - sense_number)].find(class_ = 'anthronote') is not None :
                        anthronote_cur = sensecontent[int(original_sense_number - sense_number)].find(class_ = 'anthronote')
                        dictionary.write('{\\normalsize {\it Cultural note: }')
                        dictionary.write(anthronote_cur.get_text().strip())
                        dictionary.write('} \n')
                    if sensecontent[int(original_sense_number - sense_number)].find(class_ = 'sociolinguisticsnote') is not None :
                        socio_note_cur = sensecontent[int(original_sense_number - sense_number)].find(class_ = 'sociolinguisticsnote')
                        dictionary.write('{\\normalsize {\it Social note: }')
                        dictionary.write(socio_note_cur.get_text().strip())
                        dictionary.write('} \n')
                    if sensecontent[int(original_sense_number - sense_number)].find(class_ = 'example') is not None :
                        example_cur_number = len(sensecontent[int(original_sense_number - sense_number)].find_all(class_ = 'example'))
                        if example_cur_number < 2 :
                            example_cur = sensecontent[int(original_sense_number - sense_number)].find(class_ = 'example')
                            translation_cur = sensecontent[int(original_sense_number - sense_number)].find(class_ = 'translation')
                            dictionary.write('{\\small \\sc example:} {\\normalsize \\it ')
                            dictionary.write(orthographyreplace(example_cur.get_text().strip()))
                            dictionary.write('} \n{\\small [')
                            dictionary.write(ipareplace(example_cur.get_text().strip()))
                            dictionary.write(']} \n{\\normalsize `')
                            dictionary.write(translation_cur.get_text().strip())
                            dictionary.write('\'} \n')
                        if example_cur_number > 1 :
                            example_cur = sensecontent[int(original_sense_number - sense_number)].find_all(class_ = 'example')
                            translation_cur = sensecontent[int(original_sense_number - sense_number)].find_all(class_ = 'translation')
                            example_cur_number_original = example_cur_number
                            while example_cur_number > 0 :
                                dictionary.write('{\\small \\sc example:} {\\normalsize \\it ')
                                dictionary.write(orthographyreplace(example_cur[int(example_cur_number_original - example_cur_number)].get_text().strip()))
                                dictionary.write('} \n{\\small [')
                                dictionary.write(ipareplace(example_cur[int(example_cur_number_original - example_cur_number)].get_text().strip()))
                                dictionary.write(']} \n{\\normalsize `')
                                dictionary.write(translation_cur[int(example_cur_number_original - example_cur_number)].get_text().strip())
                                dictionary.write('\'} \n')
                                example_cur_number = example_cur_number - 1
                    sense_number = sense_number - 1
                sense_number = original_sense_number
        else :
            original_sense_number = sense_number
            while sense_number > 0 :
                dictionary.write('{\\normalsize {\\bf ')
                dictionary.write(sensenumber[int(original_sense_number - sense_number)].get_text().strip())
                dictionary.write('} \n{\it ')
                dictionary_txt.write(sensenumber[int(original_sense_number - sense_number)].get_text().strip())
                dictionary_txt.write('\t')
                dictionary.write(partofspeech[int(original_sense_number - sense_number)].get_text().strip())
                dictionary.write('} \n')
                dictionary.write(definitionorgloss[int(original_sense_number - sense_number)].get_text().strip())
                dictionary.write('} \n')
                dictionary_txt.write(definitionorgloss[int(original_sense_number - sense_number)].get_text().strip())
                sense_number = sense_number - 1
            sense_number = original_sense_number
    if subentries is not None :
        #This is how I indent subentries under the main entry.
        dictionary.write('\t\\begin{adjustwidth}{6pt}{}\n')
        if subentry_number < 2 :
            dictionary.write('\t\\noindent {\\normalsize \\bf ')
            dictionary.write(orthographyreplace(sub_head.get_text().strip()))
            dictionary.write('} \n\t{\\small [')
            dictionary.write(ipareplace(sub_head.get_text().strip()))
            dictionary.write(']} \n\t{\\normalsize ')
            dictionary_txt.write(orthographyreplace(sub_head.get_text().strip()))
            dictionary_txt.write('\t [')
            dictionary_txt.write(sub_head.get_text().strip())
            dictionary_txt.write('] \t')
            if sub_pos1 is not None :
                dictionary.write('{\\it ')
                dictionary.write(sub_pos1.get_text().strip())
                dictionary.write('} \n\t')
            else :
                dictionary.write('{\\it ')
                dictionary.write(sub_pos2.get_text().strip())
                dictionary.write('} \n\t')
            dictionary.write(sub_def.get_text().strip())
            dictionary.write('} \n\n')
            dictionary_txt.write(sub_def.get_text().strip())
        if subentry_number > 1 :
            original_subentry_number = subentry_number
            while subentry_number > 0 :
                dictionary.write('\t\\noindent {\\normalsize \\bf ')
                dictionary.write(orthographyreplace(sub_head[int(original_subentry_number - subentry_number)].get_text().strip()))
                dictionary.write('} \n\t{\\small [')
                dictionary.write(ipareplace(sub_head[int(original_subentry_number - subentry_number)].get_text().strip()))
                dictionary.write(']} \n\t')
                dictionary_txt.write(orthographyreplace(sub_head[int(original_subentry_number - subentry_number)].get_text().strip()))
                dictionary_txt.write('\t [')
                dictionary_txt.write(sub_head[int(original_subentry_number - subentry_number)].get_text().strip())
                dictionary_txt.write('] \t')
                current_sub_sense = sub_senses[int(original_subentry_number - subentry_number)]
                sub_sense_number = len(current_sub_sense.find_all(class_ = 'sensenumber'))
                if current_sub_sense.find(class_ = 'sensenumber') is None :
                    dictionary.write('{\\normalsize {\\it ')
                    dictionary.write(current_sub_sense.find(class_ = 'partofspeech').get_text().strip())
                    dictionary.write('} \n\t')
                    dictionary.write(current_sub_sense.find(class_ = 'definitionorgloss').get_text().strip())
                    dictionary.write('} \n')
                elif current_sub_sense.find_all(class_ = 'sensenumber') is not None :
                    original_sub_sense_number = sub_sense_number
                    dictionary.write('{\\normalsize {\\it ')
                    dictionary.write(current_sub_sense.find(class_ = 'partofspeech').get_text().strip())
                    dictionary.write('} \n\t')
                    while sub_sense_number > 0 :
                        current_sub_def = current_sub_sense.find_all(class_ = 'definitionorgloss')
                        dictionary.write(current_sub_def[int(original_sub_sense_number - sub_sense_number)].get_text().strip())
                        dictionary.write(' ')
                        current_sub_def = current_sub_sense.find_all(class_ = 'definitionorgloss')
                        sub_sense_number = sub_sense_number -1
                    dictionary.write('} \n')
                    sub_sense_number = original_sub_sense_number
                subentry_number = subentry_number - 1
                dictionary.write('\n')
            subentry_number = original_subentry_number
        dictionary.write('\t\\end{adjustwidth}')
    if minor_headword is not None and mainheadword is None :
        if minor_type is not None :
            subentry_keep = minor_type.get_text().strip()
        if subentry_keep == 'spec' :
            continue
        else:
            dictionary.write('\\vspace{6pt} \n \\noindent {\\large \\bf ')
            dictionary.write(orthographyreplace(minor_headword.get_text().strip()))
            dictionary.write('} \n{\\small [')
            dictionary.write(ipareplace(minor_headword.get_text().strip()))
            dictionary.write(']} \n')
            if minor_reference is not None :
                dictionary.write('{\\normalsize See: \\hyperlink{')
                dictionary.write(main_reference[1:])
                dictionary.write('}{')
                dictionary.write(orthographyreplace(minor_reference.get_text().strip()))
                dictionary.write(' }}')
    dictionary.write('\n\n')
    dictionary_txt.write('\n')
    #reset minor_reference because it sometimes carries over definitions if a new minor entry is currently undefined
    minor_reference = None
dictionary.write('\end{document}')
