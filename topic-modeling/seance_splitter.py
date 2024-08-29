# - Faire un dico {annee: {}}
# - Prendre fichier par fichier
# - On lit le fichier
# - split le texte sur les séances
# - pour chaque séance
#     - on récupère son année
#     - on créé un id en parsant la date ? (peut être sha1 du texte mais moins explicite)
#     - on stocke dico[annee][id_seance] = {date, texte}

#     exemple:

#     corpus = {
#         1830: {
#             18_05_1830: {
#                 date: 8 janvier 1830,
#                 texte: blablablab....
#                 named_entities: []
#             }
#         }
#     }
#___________________________________________________________________________________________________________


import os
import re
import json

corpus = {}

for file in os.listdir("./data"):
    with open(os.path.join("./data", file), 'r', encoding='utf-8-sig') as f:
        text = f.read()
        #d'abord split par séance et ensuite on va récupère l'année courante
        #regex= capturer "séance du" et "comité du" avec ou sans majuscule, avec ou sans accent, après ou non un saut de ligne, 
        # en début de ligne ou après des espaces, après un nombre. 
        pattern = re.compile(r'(?:\n?(?:\d+e )?Comit[ée]|\n(?:\d+e )?comit[ée]|\n\s*(?:\d+e )?s[eé]ance|\n?(?:\d+e )?S[eé]ance) du')
        resultat = re.split(pattern, text)
        seances = [r for r in resultat if r.strip() != '']
        for seance in seances:
            temp = [t for t in seance[0:100].split('\n\n') if t.strip() != ""]
            date = temp[0].strip()
            res = re.search(r'\d{4}', date)
            if res:
                annee = res.group(0)
                date = date[:res.end()]
            else:
                annee = "undefined"
            texte = seance.split(date)[1].strip()
            seance_id = '_'.join(date.lower().strip().replace('é', 'e').split(' '))
            if annee not in corpus:
                corpus[annee] = {}
            corpus[annee][seance_id] = {'texte': texte, 'date': date, 'file': file}

        with open('test.json', 'w', encoding='utf-8-sig') as f:
            json.dump(corpus, f, indent=4, ensure_ascii=False)
        # print([r[0:100].strip() for r in resultat if r.strip() != ''])
        # print([seance[0:100].strip() for seance in seances])

