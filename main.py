import requests
from bs4 import BeautifulSoup
import html
import pandas as pd
import xlsxwriter
from pandas import ExcelWriter
# -*- coding: cp1252 -*-

results = []

url = "https://www.dimdi.de/static/de/klassifikationen/icd/icd-10-gm/kode-suche/htmlgm2020/#I"

request = requests.get(url).text
soup = BeautifulSoup(request, "html.parser")

links = soup.find_all("a", class_="code")
for link in links:
    link = "https://www.dimdi.de/static/de/klassifikationen/icd/icd-10-gm/kode-suche/htmlgm2020/" + link["href"]
    request = requests.get(link).text
    soup = BeautifulSoup(html.unescape(request), "html.parser")


    content = soup.find(id="classicont")

    diseases = content.find_all("div")

    for disease in diseases[1:len(diseases)-1]:
        disease_info = disease.find_all("div")
        try:
            id = html.unescape(disease.find("a").text)
            name = html.unescape(disease.find("span").text.replace("¤",""))
            name = name.replace("Ã", "ä")
            if name != "Nicht belegte Schlä¼sselnummer":
                results.append([id,name])

        except:
            pass

writer = pd.ExcelWriter("icd_codes.xlsx", engine="xlsxwriter")
df = pd.DataFrame(results, columns=["id", "krankheit"])
df.to_excel(writer,"Sheet1")
writer.save()
