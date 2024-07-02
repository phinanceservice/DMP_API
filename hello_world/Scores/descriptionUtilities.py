import re

#helper functions
def check_word(word, string):
    if word in string:
        regex = re.compile(r"\b"+word+r"\b")
        if regex.search(string):
            return True
        else:
            return False
    else:
        return False
    

def word_in_string(string, word):
    return check_word(word, string)

def check_string(word, string):
    return word in string

def initial_matches(desc_str, inp_initials_list):
    return sorted(list(set(desc_str.split()).intersection(set(inp_initials_list))))

def surname_matches(desc_str, inp_surnames_list):
    return sorted(list(set(desc_str.split()).intersection(set(inp_surnames_list))))


def first_name_matches(desc_str, inp_first_names_list):
    return sorted(list(set(desc_str.split()).intersection(set(inp_first_names_list))))


def contains_initial(desc_str, inp_initials_list):
    return any(c in inp_initials_list for c in desc_str.split())


def contains_surname(desc_str, inp_surnames_list):
    return any(check_word(name, desc_str) for name in inp_surnames_list)


def contains_first_name(desc_str, inp_first_names_list):
    return any(check_word(name, desc_str)for name in inp_first_names_list)