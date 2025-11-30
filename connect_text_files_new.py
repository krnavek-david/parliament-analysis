import os

# POUŽÍT CESTU PRO AKTUÁLNĚ SPOJOVANÉ SOUBORY
path = "E:/DP_NEW/"

with open(path + "texts_connected_new.txt", 'a', encoding='UTF-8') as output:
    for textfile in sorted(os.listdir(path + "texts/")):
        with open(path + "texts/" + textfile, 'r', encoding='UTF-8') as file:
            output.write(file.read())