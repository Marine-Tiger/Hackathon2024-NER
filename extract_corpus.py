import os
import re
import pydantic #permet de faire du typage en python
import spacy

class Chunk(pydantic.BaseModel):
    source: str
    date: str
    year: int
    text: str

def process_line_for_title_detection(line: str):
    new_text = re.sub(r'\d+e', '', line)
    return new_text
def process_document(text: str, file_path: str, documents: dict):
    # fonction qui prends un objet documents (type dict) et va le remplir de la facon suivante
    # on associe a chaque annee une liste de Chunk (portion de texte) -> {annee: [Chunk, Chunk, Chunk]}
    current_year = 0

    seance_splitters= ["séance du", "comité du"]

    # on parcours le document ligne par ligne
    # si on tombe sur une ligne qui contient une nouvelle séance / comité avec une année
    # on dit qu'a partir de maintenant toute les lignes suivantes concernent cette année (on met a jours current_year)
    # jusqu'a ce qu'on tombe sur une nouvelle ligne avec une annee...
    for line in text.split('\n'):
        processed_line=process_line_for_title_detection(line.strip().lower()).strip().lower()
        if any([processed_line.startswith(seance_splitter) for seance_splitter in seance_splitters]) :
            date_str = processed_line[10:]
            re_year = re.search(r'\d{4}', date_str)
            if (re_year):
                year = re_year.group()
                current_year = year # veut dire que l'année extraite = année actuelle --> pour toutes les prochaines lignes on sera dans la même date
                # print(processed_line,year)
                # print("====")
        else:
            if (len(processed_line) > 0 and current_year != 0):
                chunk = Chunk(source=file_path, date=date_str, year=int(current_year), text=line)
                if (not year in documents):
                        documents[year] = []
                documents[year].append(chunk)
    

def get_corpus(data_folder: str):
    documents = {}

    # on applique la logique de process_document ()
    for filename in os.listdir(data_folder):
        file_path = os.path.join(data_folder, filename)
        if os.path.isfile(file_path): #On vérifie que c'est bien un fichier
            # years = [int(year) for year in re.findall(r'\d{4}', file_path)]#va chercher les suites de 4 chiffres (année), on s'en sert pas !
            with open(file_path, 'r') as f:
                text = f.read()
                process_document(text, file_path, documents)

    return documents

def get_coref_corpus():
    # la on charge juste le fichier pickle cree par le notebook dataset_to_coref.ipynb
    # pickle permet de sauvegarder n'immporte quel variable dans un fichier pckl et de le recharger.
    # donc au lieu de relancer dataset_to_coref a chaque fois (long + pb de versions)
    # je l'ai lance une fois, puis je l'ai stocke dans un coref_corpus.pckl
    import pickle
    file = open('../coref_corpus.pckl','rb')
    data = pickle.load(file)
    return data