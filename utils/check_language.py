import string

def is_check_latin_or_printable_char(
    text: str
)-> bool:
    for c in text:
        if c.isalnum() or c in string.printable:
            return True
    return False

if __name__ == '__main__':
    text ='蛇龍動易'
    print(is_check_latin_or_printable_char(text))