# coding: utf-8

import re


# Remove html tags from src_text
def remove_html_tags(src_text):
    cleaner = re.compile('<.*?>')
    result = re.sub(cleaner, '', src_text)
    return result


# Remove emojis from src_text
def remove_emojis(src_text):
    cleaner = re.compile('[\U00010000-\U0010ffff]', flags=re.UNICODE)
    result = re.sub(cleaner, '', src_text)

    # Sometimes, 'heart' emoji is translated to 'lt3' (lower than 3: <3)
    cleaner2 = re.compile('lt3')
    result = re.sub(cleaner2, '', result)
    return result


# Remove http(s) links
def remove_http_links(src_text):
    cleaner = re.compile("http\S+")
    result = re.sub(cleaner, '', src_text)
    return result


# Remove all special characters and punctuation
def remove_special_chars(src_text):
    cleaner = re.compile("[^A-Za-z0-9'’ -]+")
    result = re.sub(cleaner, '', src_text)
    return result


# Remove all accents
def remove_accents(src_text):
    fr_accents = ['à', 'â', 'ä', 'é', 'è', 'ê', 'ë', 'ï', 'î', 'ö', 'ô', 'û', 'ü', 'ù', 'ç']
    without_accents = ['a', 'a', 'a', 'e', 'e', 'e', 'e', 'i', 'i', 'o', 'o', 'u', 'u', 'u', 'c']

    i = 0
    while i < len(src_text):
        if src_text[i] in fr_accents:
            if i+1 != len(src_text):
                src_text = "".join((src_text[:i], without_accents[fr_accents.index(src_text[i])], src_text[i+1:]))
            else:
                src_text = "".join((src_text[:i], without_accents[fr_accents.index(src_text[i])], ""))
        i += 1

    return src_text


# Convert src_text to lowercase
def lowercase_text(src_text):
    return src_text.lower()


# Remove all spaces in 'src_text
def remove_spaces(src_text):
    return src_text.replace(" ", "")


# Remove html tags, emojis, http(s) links, special characters, punctuation.
# Replace accents and uppercase
def clean_html_text(src_text):
    return remove_special_chars(remove_accents(lowercase_text(remove_http_links(remove_emojis(remove_html_tags(src_text))))))