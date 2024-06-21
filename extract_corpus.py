import os
import re
import re
import pydantic #permet de faire du typage en python

class Chunk(pydantic.BaseModel):
    source: str
    date: str
    year: int
    text: str

def process_document(text: str, file_path: str, documents: dict):

    current_year = 0

    seance_splitters= ["séance du", "comité du"]

    for line in text.split('\n'):
        processed_line=line.strip().lower()
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
                chunk = Chunk(source=file_path, date=date_str, year=current_year, text=line)
                if (not year in documents):
                        documents[year] = []
                documents[year].append(chunk)

def get_corpus(data_folder: str):
    documents = {}

    for filename in os.listdir(data_folder):
        file_path = os.path.join(data_folder, filename)
        if os.path.isfile(file_path): #On vérifie que c'est bien un fichier
            # years = [int(year) for year in re.findall(r'\d{4}', file_path)]#va chercher les suites de 4 chiffres (année), on s'en sert pas !
            with open(file_path, 'r') as f:
                text = f.read()
                process_document(text, file_path, documents)

    return documents
