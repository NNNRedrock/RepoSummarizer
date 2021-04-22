from lexrank import STOPWORDS, LexRank
import pandas as pd

documents = []
sentences = []
reponames = []

df = pd.read_csv('train.csv', index_col='Repo Name')
df2 = pd.read_csv('train.csv')
df3 = pd.read_csv('test.csv')

for reponame in df2['Repo Name']:
    reponames.append(reponame)

reponames = set(reponames)

for reponame in reponames:
    documents.append(df.loc[reponame]['Commits'])

lxr = LexRank(documents, stopwords=STOPWORDS['en'])

for j in range(0,3):
    for i in range(0,300):
        sentences.append(df3.iloc[i+300*j]['Commits'])

    summary = lxr.get_summary(sentences, summary_size= 100, threshold=.3)
    sentences = []
    print(summary)