import pandas as pd
import re
import nltk
nltk.download('punkt')
nltk.download('brown')
from nltk.corpus import brown
nltk.download('words')
words = set(brown.words())
from sklearn.feature_extraction.text import TfidfVectorizer
import string
from main import transform_file
stemmer = nltk.stem.porter.PorterStemmer()
remove_punct = dict((ord(char), None) for char in string.punctuation)

def clean_text(text):
    text = re.sub(r'\b[a-zA-Z]\b', '', text)
    text = re.sub('https?://\S+|www\.\S+', '', text)
    text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub('\n', '', text)
    text = re.sub('\t', '', text)
    text = re.sub('[^\x00-\x7F]', '', text)
    text = re.sub('\w*\d\w*', '', text)
    text = re.sub('[^\x00-\x7F\x80-\xFF\u0100-\u017F\u0180-\u024F\u1E00-\u1EFF]', '', text)
    text = str(text).lower()
    text = " ".join(w for w in nltk.wordpunct_tokenize(text) if w.lower() in words or not w.isalpha())
    text = re.sub('¢', '', text)
    return text

def stem_tokens(tokens):
    return [stemmer.stem(item) for item in tokens]

def normalize(text):
    return stem_tokens(nltk.word_tokenize(text.lower().translate(remove_punct)))

vectorizer = TfidfVectorizer(tokenizer=normalize, stop_words='english')

def cosine_sim(text1, text2, k, df):
    tfidf = vectorizer.fit_transform([text1, text2])
    result = (((tfidf * tfidf.T).A)[0,1])
    if result > 0.5:
      df.loc[k,'status'] = 1
    return df

def calc_points(user_points):  
  points = sum((user_points.weights).astype(int) * (user_points.status).astype(int))
  total = sum((user_points.weights).astype(int))
  total_points = (points * 100)/ total
  return total_points


def points_results(filename, file_class):
  file_path = 'jobs_description/'
  job_description_file = file_path + str(file_class) + '.csv'

  df = pd.read_csv(job_description_file, index_col = False, dtype=str)
  df['status'] = 0
  df['features'] = df['features'].str.lower()

  job_df = transform_file(filename)
  job_df=job_df.iloc[:,0]

  job_df = job_df.apply(lambda x: clean_text(x))
  job_df.reset_index(drop=True, inplace=True)

  df['status'] = 0
  size = 5
  min = 0
  limit = len(job_df[0]) - size

  for t in range(1):
    splitted = job_df[t].split()
    qtd_reqs = len(df)
    for k in range(qtd_reqs):
      size = len(df['features'][k].split())

      for i in range(limit):
        min = i
        max = min + size
        sentence = ' '.join(splitted[min:max])
        df = cosine_sim(sentence, df['features'][k], k, df)
        user_points = df
    text = '<br><br>You have covered all of this requirements: <br>'

    for index, row in user_points.iterrows():
      if (row['status']) == 1:
        feature_desc = row['features']
        feature_desc = feature_desc[0].upper() + feature_desc[1:]
        text = text + '-' + feature_desc + ' <br> '

    total_p = calc_points(user_points)
    df['status'] = 0

  return total_p, text
