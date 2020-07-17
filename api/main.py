import os
import pdftotext
import docx2txt
import pandas as pd
import re
from werkzeug.datastructures import FileStorage

def save_csv(text,file):
    df = pd.DataFrame(columns=['text'])
    df = df.append({
        "text": text
        }, ignore_index=True)
    return (df)

def transform_file(filename):
    file_path = ''
    file = filename
    if file.endswith(".doc"):
        try:
            olddoc = os.path.join(file_path,file)
            doc = olddoc.replace(" ","_").replace("(","_").replace(")","_")
            os.rename(olddoc, doc)
            docx = doc + 'x'
            os.system('antiword ' + doc + ' > ' + docx)
            with open(os.path.join(file_path,docx)) as f:
                text = f.read()
            os.remove(os.path.join(file_path,docx))
            text = re.sub(r'\s',' ',text)
        except Exception as e:
            print(e)

    elif file.endswith(".pdf"):
        with open(os.path.join(file_path,file), "rb") as f:
            pdf = pdftotext.PDF(f)
        text = ("\n\n".join(pdf))
        text = re.sub(r'\s',' ',text)

    elif file.endswith(".docx"):
        text = docx2txt.process(os.path.join(file_path,file))
        text = re.sub(r'\s',' ',text)

    return save_csv(text,file)

