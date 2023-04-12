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
soup = BeautifulSoup(request, "html.parser", from_encoding="utf-8")

links = soup.find_all("a", class_="code")
for link in links[:5]:
    link = "https://www.dimdi.de/static/de/klassifikationen/icd/icd-10-gm/kode-suche/htmlgm2020/" + link["href"]
    request = requests.get(link).text
    soup = BeautifulSoup(html.unescape(request), "html.parser", from_encoding="utf-8")


    content = soup.find(id="classicont")

    diseases = content.find_all("div", class_="Category1")
    for disease in diseases:
        disease_result = {}
        subcode_list = []
        parent_id = html.unescape(disease.find("a").text)
        parent_name = html.unescape(disease.find("span").text).replace("Ã¼", "ü")
        parent_name = parent_name.replace("Ã¤", "ä")
        subcodes = content.find_all(class_="Category2")
        for subcode in subcodes:
            if parent_id.replace(".-","") in subcode.find("a").text:
                subcode_id = html.unescape(subcode.find("a").text)
                subcode_name = html.unescape(subcode.find("span").text)
                subcode_name = subcode_name.replace("Ã¼", "ü")
                subcode_name = subcode_name.replace("Ã¤", "ä")
                subcode_name = subcode_name.replace("Ã¶", "ö")
                subcode_list.append([subcode_id, subcode_name])

        disease_result["code"] = parent_id.decode("UTF-8")
        disease_result["name"] = parent_name.decode("UTF-8")
        disease_result["dependencies"] = subcode_list.decode("UTF-8")

        if disease_result not in results:
            results.append(disease_result)

for result in results:
    print(result)







#     for disease in diseases[1:len(diseases)-1]:
#         disease_info = disease.find_all("div")
#         try:
#             id = html.unescape(disease.find("a").text)
#             name = html.unescape(disease.find("span").text.replace("¤",""))
#             name = name.replace("Ã", "ä")
#             if name != "Nicht belegte Schlä¼sselnummer":
#                 results.append([id,name])
#
#         except:
#             pass
#
# writer = pd.ExcelWriter("icd_codes.xlsx", engine="xlsxwriter")
# df = pd.DataFrame(results, columns=["id", "krankheit"])
# df.to_excel(writer,"Sheet1")
# writer.save()
