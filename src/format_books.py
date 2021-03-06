'''
Taking in a txt file and formatting the txt file in a way that can be fed into my model
'''
import pandas as pd
import numpy as np
import re
from nltk import sent_tokenize

def load_data(filename):
    '''
    INPUT: Filename
    OUTPUT: Opened filename
    '''
    f = open(filename)
    return f.read()

def get_rid_of_weird_characters(book):
    '''
    INPUT: Book file
    OUTPUT: Cleaned Book file
    '''
    book = re.sub('[^A-Za-z0-9,;.?!'']+', ' ', book)
    return book

def get_sections(book):
    '''
    INPUT: Book text file
    OUTPUT: Split book text file
    '''
    return book.split('\n\n\n\n\n\n')

def chapter_paragraph_tag(book):
    '''
    INPUT: Book text file
    OUTPUT: Tagged book text file
    '''
    chapter_book = []
    chapter_indicators = ["Chapter", "ONE", "TWO", "THREE", "FOUR", "FIVE", "SIX", "SEVEN", "EIGHT", "NINE", "TEN", "ELEVEN", "TWELVE", "THIRTEEN"]

    for section in book:
        section_split = section.split()
        if any(ind in section_split[:2] for ind in chapter_indicators):
            section = " <CHAPTERBEGIN> " + section
        else:
            section = " <PARAGRAPH> " + section
        chapter_book.append(section)
    return chapter_book

def combine_strings_split_on_chapter(book):
    '''
    INPUT: Book text file
    OUTPUT: Split book text file by chapter tag
    '''
    book = " ".join(book)
    return book.split("<CHAPTERBEGIN>")

def split_by_section(book):
    '''
    INPUT: Book text file
    OUTPUT: Split book text file
    '''
    book_list = []
    for chapter in book:
        split_chapter = chapter.split("<PARAGRAPH>")
        paragraph_by_chapter = [s_chapter for s_chapter in split_chapter]
        book_list.append(paragraph_by_chapter)
    return book_list

def format_sentences(book):
    '''
    INPUT: Book text file
    OUTPUT: List of each text file section tokenized
    '''
    book_list = []
    paragraph_list = []

    for chapter in book:
        chapter_list = []
        for paragraph in chapter:
            paragraph_tok = sent_tokenize(paragraph)
            chapter_list.append(paragraph_tok)
        book_list.append(chapter_list)
    return book_list

def split_by_percentage(book, n = 10):
    '''
    Splitting the book into n number of sections
    INPUT: Book text file
    OUTPUT: Book text file section
    '''
    book_sections = []
    sentences_in_section = len(book)/n
    for i in range(0,n):
        section = book[sentences_in_section * i: sentences_in_section * (i+1)]
        book_sections.append(section)
    return book_sections

if __name__ == '__main__':

    '''
    ----------------- Splitting by Chapters -----------------
    '''
    dirty_book = load_data('booktxt/Moonwalking With Einstein.txt')
    sliced_book = get_sections(dirty_book)
    kinda_clean_book = [get_rid_of_weird_characters(section) for section in sliced_book]
    more_clean_book = chapter_paragraph_tag(kinda_clean_book)
    combined = combine_strings_split_on_chapter(more_clean_book) #A list of chapters.
    split = split_by_section(combined)

    formatted_sentence = format_sentences(split)


    '''
    ----------------- Splitting by Percentages -----------------
    '''
    book = get_rid_of_weird_characters(dirty_book)
    all_sentences, book_sections = split_by_percentage(sent_tokenize(book), n = 10)
