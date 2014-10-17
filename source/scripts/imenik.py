#!/usr/bin/env python

"""
Telefonski imenik
Location: https://github.com/schef/horvat-elektronika/source/scripts
"""

__author__ = 'Stjepan Horvat (zvanstefan@gmail.com)'
__copyright__ = 'Copyright (c) 2014 Stjepan Horvat'
__license__ = 'GNU'
__vcs_id__ = '$Id$'
__version__ = '1.0'

import sys
from argparse import ArgumentParser
import requests #used for POST request
from bs4 import BeautifulSoup #used form html parsing
from colorama import Fore #used form colouring

ap = ArgumentParser()
ap.add_argument('-t', '--tko', type=str, help="WHO are you searching for")
ap.add_argument('-g', '--gdje', type=str, help="WHERE are you searching from")
args = ap.parse_args()

#prints the welcome message
print("Telefonski imenik")

#TODO:if no argument are added it asks you for the input
if (args.tko):
    tko_input = args.tko
else:
    tko_input = input("Tko: ")
if (args.gdje):
    gdje_input = args.gdje
else:
    gdje_input = input("Gdje: ")

#submit form defined by the webpage coder
url = 'http://imenik.tportal.hr'
data = {
    "newSearch" : "1",
    "action" : "pretraga",
    "type" : "brzaPretraga",
    "tko" : tko_input,
    "gdje" : gdje_input
}

print("Searching...")
r = requests.post(url, data)

#TODO:save if user arg required it
#with open("requests_results.html", "w") as f:
#    f.write(bytes.decode(r.content))

soup = BeautifulSoup(bytes.decode(r.content))


lista = [] #list initialization
index = 0 #used for creating sublists of specific name found.

#store addresses found to list
#it searches for name and attrs={}
for tag in soup.find_all(["div", "li"], class_=["resultsTitle", "secondColumn", "ostaliPodaciLevel-1", "imenikTelefon"]):
    try:
        #this searches for a number
        if ['imenikTelefon'] in (tag.attrs.values()):
            lista[index].append(tag.contents[0])
        #this searches for a address
        elif ['secondColumn', ''] in (tag.attrs.values()):
            lista[index].append(tag.contents[1].text.strip())
            lista[index].append(tag.contents[3].text.strip())
        if len(lista[index]) == 4:
            index += 1
    except IndexError:
        #if list index doesn't exist create a new one
        lista.append([])
        #this searches for a name
        if ['resultsTitle'] in (tag.attrs.values()):
            lista[index].append(tag.contents[0])


#TODO:check the list and copy the number to xclip if requred by user by args
if len(lista) == 0:
        print("Nothing found!")
        sys.exit()
elif len(lista) == 1:
    #print the first and only element
    print("Only 1 item found:")
    print("[", Fore.GREEN + str(1) + Fore.RESET, "] ", Fore.BLUE + lista[0][0] + Fore.RESET, " ", lista[0][1], " ", lista[0][2], " ", lista[0][3], sep='')
    print(lista[0][3])
elif len(lista) > 1:
    #print adresses found from list
    print("Found", len(lista), "items:")
    for i in range(len(lista)):
        print("[", Fore.GREEN + str(i) + Fore.RESET, "] ", Fore.BLUE + lista[i][0] + Fore.RESET, " ", lista[i][1], " ", lista[i][2], " ", lista[i][3], sep='')
    user_input = input("Some input please: ")
    print(lista[int(user_input)][3])
