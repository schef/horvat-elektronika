#!/usr/bin/env python
url = 'http://imenik.tportal.hr/show'
print("Telefonski imenik")
tko_input = input("Tko: ")
gdje_input = input("Gdje: ")
data = {
    "newSearch":"1",
    "action":"pretraga",
    "type":"brzaPretraga",
    "tko":tko_input,
    "gdje":gdje_input
}

import requests

r = requests.post(url, data)
with open("requests_results.html", "w") as f:
    f.write(bytes.decode(r.content))

from bs4 import BeautifulSoup
soup = BeautifulSoup(bytes.decode(r.content))

from colorama import Fore
verbose = 0

import logging
logging.basicConfig(level=logging.WARNING, format="%(msg)s")
if verbose:
    logging.getLogger().setLevel(logging.DEBUG)
LOG = logging.getLogger('logtest')

lista = []
i = 0
#store addresses found to list
for tag in soup.find_all(["div", "li"], class_=["resultsTitle", "secondColumn", "ostaliPodaciLevel-1", "imenikTelefon"]):
        try:
            if ['imenikTelefon'] in (tag.attrs.values()):
                lista[i].append(tag.contents[0])
            elif ['secondColumn', ''] in (tag.attrs.values()):
                lista[i].append(tag.contents[1].text.strip())
                lista[i].append(tag.contents[3].text.strip())
            if len(lista[i]) == 4:
                i = i + 1
        except IndexError:
            lista.append([])
            if ['resultsTitle'] in (tag.attrs.values()):
                lista[i].append(tag.contents[0])
#print adresses found from list
for i in range(len(lista)):
        print("[", Fore.GREEN + str(i) + Fore.RESET, "] ", Fore.BLUE + lista[i][0] + Fore.RESET, " ", lista[i][1], " ", lista[i][2], " ", lista[i][3], sep='')

if len(lista) > 1:
        user_input = input("Some input please: ")

print(lista[int(user_input)][3])
