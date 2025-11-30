import os
import re
import time
from tqdm import tqdm


# CESTY ZMĚNIT NA AKTUÁLNĚ ANALYZOVANÉ SUBKORPUSY
conllu_path = "E:/DP_NEW/parties_by_year_no_leaders/annotated/"
output_path = "E:/DP_NEW/parties_by_year_no_leaders/indices/"

def compare_verts(a, b):
    tokencount = 0
    for token in a:
        if token != b[tokencount]:
            print(token + " in a = " + b[tokencount] + " in b")
        else:
            print(token + " in a = " + b[tokencount] + " in b")
        tokencount += 1
    tokencount = 0
    for token in b:
        if token != a[tokencount]:
            print(token + " in b = " + a[tokencount] + " in a")
        else:
            print(token + " in b = " + a[tokencount] + " in a")
        tokencount += 1
    
def compare_verts_simple(a, b):
    tokencount = 0
    for token in a:
        print(token + " in a = " + b[tokencount] + " in b")
        if token != b[tokencount]:
            time.sleep(1)
        tokencount += 1


def parse_vert(filename):
    lines = open(conllu_path + filename, "r", encoding='UTF-8').readlines()
    filtered_lines = []
    for i in tqdm(range(len(lines)), desc=("parsing vertical from " + filename), colour="GREEN"):
        if len(lines[i]) > 1 and lines[i][0] != "#":
            filtered_lines.append(lines[i].split("\t")[:4])
    return filtered_lines

def lemmas_pos_forms(vert):
    
    lemmas = []
    pos = []
    forms = []
    for i in tqdm(range(len(vert)), desc="extracting lemmas and pos", colour="CYAN"):
        if len(vert[i]) > 3:
            lemmas.append(vert[i][2])
            pos.append(vert[i][3])
            forms.append(vert[i][1])

    lemmas_lc = [lemma.lower() for lemma in lemmas]
    forms_lc = [form.lower() for form in forms]

    return lemmas_lc, pos, forms_lc

def remove_punct_and_aux(vert):
    count = 0

    # odstranění interpunkce
    no_punct = [line for line in vert if line[3] != 'PUNCT']

    # odstranění aby, kdyby atd.
    count = 0
    no_aby = no_punct
    while(count != len(no_aby)):
        if no_aby[count][1].startswith("aby"):
            no_aby[count][2] = "aby"
            no_aby[count][3] = "SCONJ"
            no_aby.pop(count+1)
            no_aby.pop(count+1)
        if no_aby[count][1].startswith("kdyby"):
            no_aby[count][2] = "když"
            no_aby[count][3] = "SCONJ"
            no_aby.pop(count+1)
            no_aby.pop(count+1)
        count += 1
    return no_aby

def extract_from_vert(vert, column):
    column_values = []
    for row in vert:
        if len(row) > column:
            column_values.append(row[column])
            # print(row[column])
    return(column_values)

# vypočítá TTR pro daný seznam tokenů

def ttr(forms):
    types = list(set(forms))
    return len(types) / len(forms)

# vypočítá MATTR s nastavitelnou velikostí okna pro daný seznam tokenů

def mattr(forms, l):
    types = []
    position = 0
    ttr_list = []
    for i in tqdm(range(len(forms) - l), desc="calculating TTR", colour="BLUE"):
        ttr_list.append(ttr(forms[i:i+l]))
    return sum(ttr_list) / len(ttr_list)

# vypočítá MAMR s nastavitelnou velikostí okna pro daný seznam tokenů

def mamr(forms, lemmas, l):
    mattr_forms = mattr(forms, l)
    # print(mattr_forms)
    mattr_lemmas = mattr(lemmas, l)
    # print(mattr_lemmas)
    return mattr_forms - mattr_lemmas

def mattr_mamr(forms, lemmas, l):
    mattr_forms = mattr(forms, l)
    # print(mattr_forms)
    mattr_lemmas = mattr(lemmas, l)
    # print(mattr_lemmas)
    return mattr_forms, mattr_forms - mattr_lemmas

# vypočítá průměrnou vzdálenost sloves ve vertikále

def verb_distance(pos):
    dist = 0
    avg_dist = 0
    v_count = 0
    for i in tqdm(range(len(pos)), desc="calculating verb distance", colour="MAGENTA"):
        if pos[i] == 'VERB':
            if dist > 0:
                v_count += 1
                avg_dist += dist
            dist = 0
        else:
            dist += 1
    return avg_dist / v_count

def verb_distance_new(pos):
    distances = [[]]
    for token in pos:
        if token != 'VERB':
            distances[-1].append(token)
        else:
            distances.append([])
    return sum([len(distance) for distance in distances])

# vypočítá aktivitu z vertikály

def activity(pos):
    adj = pos.count('ADJ')
    verb = pos.count('VERB')
    return verb / (verb + adj)

# vypočítá průměrnou délku tokenu

def avg_token_type_length(forms):
    types = list(set(forms))
    len_sum_tokens = 0
    len_sum_types = 0
    for i in tqdm(range(len(forms)), desc="calculating average token length", colour="YELLOW"):
        len_sum_tokens += len(forms[i])
    for i in tqdm(range(len(types)), desc="calculating average type length", colour="YELLOW"):
        len_sum_types += len(types[i])
    return (len_sum_tokens / len(forms), len_sum_types / len(types))

# vypočítá průměrnou délku tokenu

def avg_type_length(forms):
    types = list(set(forms))
    
    for type in types:
        len_sum += len(type)
    
    return len_sum / len(types)

# vypočítá průměrnou délku věty

def avg_sent_length(vert):
    lengths = []
    current_length = 0
    for i in tqdm(range(len(vert)), desc="calculating average sentence length", colour="YELLOW"):
        if vert[i][0] == "1":
            if current_length > 0:
                lengths.append(current_length)
            current_length = 1
        else:
            current_length += 1
    lengths.append(current_length)
    return sum(lengths) / len(lengths)

def lexical_density(pos):
    return (pos.count('NOUN') + pos.count('ADJ') + pos.count('VERB') + pos.count('ADV')) / len(pos)

def calc_indices(v):
    print(v + ":")
    # text = prepare(textname)
    vertical = remove_punct_and_aux(parse_vert(v))
    l_p_f = lemmas_pos_forms(vertical)
    lemmas = l_p_f[0]
    pos = l_p_f[1]
    forms = l_p_f[2]
    textlength = len(forms)
    if textlength < 500:
        return v, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
    vd = verb_distance(pos)
    q = activity(pos)
    atoktypl = avg_token_type_length(forms)
    asl = avg_sent_length(vertical)
    mm100 = mattr_mamr(forms, lemmas, 100)
    mm500 = mattr_mamr(forms, lemmas, 500)
    print("number of words: " + str(len(forms)))
    print("number of lemmas: " + str(len(lemmas)))
    print("text length: " + str(textlength))
    print("VD: " + str(vd))
    print("Q: " + str(q))
    print("average token length: " + str(atoktypl[0]))
    print("average type length: " + str(atoktypl[1]))
    print("average sentence length: " + str(asl))
    print("MATTR (L=100): " + str(mm100[0]))
    print("MATTR (L=500): " + str(mm500[0]))
    print("MAMR (L=100): " + str(mm100[1]))
    print("MAMR (L=500): " + str(mm500[1]))
    ld = lexical_density(pos)
    print("LD: " + str(ld))
    return v, textlength, vd, q, atoktypl[0], atoktypl[1], asl, mm100[0], mm500[0], mm100[1], mm500[1], ld

verticals = os.listdir(conllu_path)
verticals.sort()
print(verticals)


with open(output_path + "indices_new3.csv", 'a', encoding='UTF-8') as file:
    file.write("textname;textlength;vd;q;avg_token_length;avg_type_length;avg_sent_length;mattr100;mattr500;mamr100;mamr500;ld\n")
    for vertical in verticals:
        indices = calc_indices(vertical)
        print(indices)
        file.write(indices[0] + ";" 
                   + str(indices[1]) + ";" 
                   + str(indices[2]) + ";" 
                   + str(indices[3]) + ";" 
                   + str(indices[4]) + ";" 
                   + str(indices[5]) + ";" 
                   + str(indices[6]) + ";" 
                   + str(indices[7]) + ";" 
                   + str(indices[8]) + ";" 
                   + str(indices[9]) + ";" 
                   + str(indices[10]) + ";"
                   + str(indices[11]) + "\n")
