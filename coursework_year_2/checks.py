from datetime import datetime
import re


def is_date(string):
    try:
        datetime.strptime(string, '%Y/%m/%d')
        return True
    except ValueError:
        return False


def is_phone(string):
    if string[0] == '8' and len(string) == 11:
        return is_int(string)
    elif string[:2] == '+7' and len(string) == 12:
        return is_int(string[1:])
    else:
        return False


def is_email(email):
    regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'
    if re.search(regex, email):
        return True
    else:
        return False


def is_data_filled(array):
    for el in array:
        if el == '':
            return False
    return True


def is_ssn_inn_passp(string, type_):
    if type_ == 'inn' and len(string) == 14 or type_ == 'ssn' and len(string) == 11 or type_ == 'passport' and \
            len(string) == 10:
        return is_int(string)
    else:
        return False


def is_int(string):
    try:
        int(string)
        return True
    except ValueError:
        return False
