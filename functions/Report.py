"""
Reports command usage and errors.
A way to keep track of which commands are really used, detect use abuse (we can easily detect DOS and spam), and errors.
"""

from os.path import getsize

def _guarantee():
    """ Guarantees file existance on initialization """
    with open('report.txt','a') as file:
        if file.tell() != 0:
            return
    with open('report.txt','w') as fille:
        fille.write('')
        
def _limit():
    """ Assures report file doesn't exceed the 5MB limit. """
    _guarantee()
    overflow = getsize('report.txt') - 1024 * 1024 * 2
    if overflow > 0:
        with open('report.txt') as file:
            content = file.read()
        content=content[overflow:]
        with open('report.txt','w') as file:
            file.write(content)

def write(content: str):
    with open('report.txt','a') as file:
        file.write(content+"\n\n")