#!/usr/bin/env python

import requests #used for POST request
from bs4 import BeautifulSoup #used form html parsing
from colorama import Fore #used form colouring

#prints the welcome message
print("Telefonski imenik")

#TODO:if no argument are added it asks you for the input
tko_input = input("Tko: ")
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

#print adresses found from list
for i in range(len(lista)):
    print("[", Fore.GREEN + str(i) + Fore.RESET, "] ", Fore.BLUE + lista[i][0] + Fore.RESET, " ", lista[i][1], " ", lista[i][2], " ", lista[i][3], sep='')

#TODO:check the list and copy the number to xclip
if len(lista) == 0:
        print("Nothing found!")
elif len(lista) == 1:
        print(lista[0][3])
elif len(lista) > 1:
        user_input = input("Some input please: ")
        print(lista[int(user_input)][3])
