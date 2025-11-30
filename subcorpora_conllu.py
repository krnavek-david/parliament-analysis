from conllu import parse
import requests
import re
import os
import time

ud_pipe = 'http://lindat.mff.cuni.cz/services/udpipe/api/process'

conllu_header = "# generator = UDPipe 2, https://lindat.mff.cuni.cz/services/udpipe\n# udpipe_model = czech-pdt-ud-2.15-241121\n# udpipe_model_licence = CC BY-NC-SA\n# newdoc\n# newpar"

def split_string_to_chunks(text, chunk_length):
    # Rozdělení řetězce na jednotlivé řádky
    lines = text.splitlines()
    
    chunks = []
    while len(lines) > 0:
        if len(lines) > chunk_length:
            chunks.append("\n".join(lines[:chunk_length]))
            lines = lines[chunk_length:]
            print(chunks[-1][:100])
        else:
            chunks.append("\n".join(lines))
            print(chunks[-1][:100])
            return chunks


def correct_sent_id(vert):
    joined = conllu_header
    sent_list = re.split(r"\n\# sent_id = [0-9]*\n", vert)[1:]
    sent_id = 1
    for sent in sent_list:
        joined += "\n# sent_id = " + str(sent_id) + "\n" + sent
        sent_id += 1
    joined = joined.replace("\n\n\n", "\n\n")
    return joined
    


# CESTU ZMĚNIT NA AKTUÁLNĚ ANOTOVANÉ SUBKORPUSY
path = "E:/DP_NEW/parties_by_year_no_leaders/"

chunk_size = 100

for text in os.listdir(path + "texts/"):

    if not os.path.isfile(path + "annotated/conllu_" + text):

        with open(path + "texts/" + text, 'r', encoding='UTF-8') as file:
            textcontent = file.read()

        if len(textcontent.splitlines()) > chunk_size - 1:
            print("rozdělování " + text + " po " + str(chunk_size) + " řádcích")
            splitted_text = split_string_to_chunks(textcontent, chunk_size)
            print("rozděleno na " + str(len(splitted_text)) + " částí:")
            for chunk in splitted_text:
                print(len(chunk.splitlines()))
            chunknumber = 1
            ud_pipified_json_data = ""
            for chunk in splitted_text:
                print("posílání " + str(chunknumber) + ". části " + text + " z " + str(len(splitted_text)) + " do udpipe")
                ud_pipified_data = requests.post(ud_pipe, data={'tokenizer': '', 'tagger': '', 'parser': ''},\
                    files={'data': chunk})
                ud_pipified_json_data += ud_pipified_data.json()['result'].replace(conllu_header, "")
                chunknumber += 1
            with open(path + "annotated/conllu_" + text, "w", encoding='UTF-8') as f:
                # f.write(correct_sent_id(ud_pipified_json_data))
                f.write(ud_pipified_json_data)
                print("zápis všech částí do souboru dokončen")
        else:
            print("posílání " + text + " do udpipe")

            ud_pipified_data = requests.post(ud_pipe, data={'tokenizer': '', 'tagger': '', 'parser': ''},\
                files={'data': open(path + "texts/" + text, encoding='UTF-8')})
            ud_pipified_json_data = ud_pipified_data.json()['result']

            print("anotováno, probíhá zápis do souboru")
            with open(path + "annotated/conllu_" + text, "w", encoding='UTF-8') as f:
                f.write(ud_pipified_json_data)
                print("zápis do souboru dokončen")
    else:
        print("soubor " + path + "annotated/conllu_" + text + " již existuje")