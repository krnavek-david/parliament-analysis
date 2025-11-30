import os

BASE_PATH = "E:/DP_new/parties_new/annotated/"
OUTPUT_PATH = "E:/DP_new/parties_new/output/"
verticals = os.listdir(BASE_PATH)
print(verticals)

years = range(2013, 2024)
parties = ["ANO", "ČSSD", "KDU-ČSL", "KSČM", "ODS", "Piráti", "SPD", "STAN", "TOP09", "Úsvit"]

for party in parties:
    with open(OUTPUT_PATH + "conllu_" + party + ".txt", "a", encoding="UTF-8") as f_output:
        for year in years:
            if "conllu_" + str(year) + "_" + party + ".txt" in verticals:
                with open(BASE_PATH + "conllu_" + str(year) + "_" + party + ".txt", "r", encoding="UTF-8") as f_input:
                    vert = f_input.read()
                    f_output.write(vert)