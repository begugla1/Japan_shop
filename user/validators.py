import string


def valid_number(number):
    try:
        data = {
            1: lambda x: number[0] == '+' or number[0] in string.digits,
            2: all(list(map(lambda x: str(x).isdigit(), number[1:])))
        }
    except TypeError:
        return True
    
    return all(data.values())
