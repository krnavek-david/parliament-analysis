import os

# POUŽÍT CESTU PRO AKTUÁLNĚ SPOJOVANÉ SOUBORY
path = "E:/DP_NEW/"

with open(path + "meta_connected.txt", 'a', encoding='UTF-8') as output:
    output.write("Text_ID\tID\tTitle\tDate\tBody\tTerm\tSession\tMeeting\tSitting\tAgenda\tSubcorpus\tLang\tSpeaker_role\tSpeaker_MP\tSpeaker_minister\tSpeaker_party\tSpeaker_party_name\tParty_status\tParty_orientation\tSpeaker_ID\tSpeaker_name\tSpeaker_gender\tSpeaker_birth\tTopic\n")
    for textfile in sorted(os.listdir(path + "meta/")):
        if "meta-en" not in textfile:
            with open(path + "meta/" + textfile, 'r', encoding='UTF-8') as file:
                for line in file.readlines()[1:]:
                    output.write(line)

# výstup nutno upravit:
# ANO2011 -> ANO
# CSSD -> ČSSD
# TOP09-S -> TOP09
# Usvit -> Úsvit