'''
Created on Apr 3, 2013

@author: FelixLiu
'''
char_lower = "a"
char_upper = "A"
number = "0"
other = "_"

def get_word_class(token):
    ret = ""
    for c in token:
        if c.isalpha():
            if c.islower():
                ret += char_lower
            else:
                ret += char_upper
        elif c.isdigit():
            ret += number
        else:
            ret += other
    return ret

def get_brief_word_class(token):
    ret = ""
    for c in token:
        if c.isalpha():
            if c.islower():
                ret = __append_char__(ret, char_lower)
            else:
                ret = __append_char__(ret, char_upper)
        elif c.isdigit():
            ret = __append_char__(ret, number)
        else:
            ret = __append_char__(ret, other)
    return ret

def __append_char__(ret, char):
    if len(ret) > 0 and ret[-1] == char:
        return ret
    else:
        ret += char
        return ret