import os
import re


path = "E:/DP_NEW/"

with open(path + "meta_all_fixed.txt", 'r', encoding='UTF-8') as metafile:
    metadata = [line.split('\t') for line in metafile.readlines()][1:]

with open(path + "texts_connected_new.txt", 'r', encoding='UTF-8') as textfile:
    texts = [line.split('\t') for line in textfile.readlines()]

textdict = {}

for line in texts:
    textdict[line[0]] = line[1]

metayears = {
    '2013': [],
    '2014': [],
    '2015': [],
    '2016': [],
    '2017': [],
    '2018': [],
    '2019': [],
    '2020': [],
    '2021': [],
    '2022': [],
    '2023': [],
}

for line in metadata:
    metayears[line[3][:4]].append(line)

for year, speechlist in metayears.items():

    parties = {
        'ANO': "",
        'ČSSD': "",
        'KDU-ČSL': "",
        'KSČM': "",
        'ODS': "",
        'Piráti': "",
        'SPD': "",
        'STAN': "",
        'TOP09': "",
        'Úsvit': "",
        '-': ""
    }

    for i in range(len(speechlist)):
        if speechlist[i][19] not in ("AndrejBabis.1954", "PetrFiala.1964") and speechlist[i][15] in ("ANO", "ODS"):
            parties[speechlist[i][15]] += textdict[speechlist[i][1]]

    for k, v in parties.items():
        if v != "":
            with open(path + "parties_by_year_no_leaders/" + year + "_" + k + "_bez_lidra.txt", 'w', encoding='UTF-8') as output:
                output.write(re.sub(r"\[\[[^\]]*\]\]", "", v).replace("  ", " "))
    