from repo_sum.lsa_summarizer import LsaSummarizer
import nltk
import pandas as pd
import torch
import re
from transformers import T5Tokenizer, T5ForConditionalGeneration
nltk.download("punkt", quiet=True)
nltk.download("stopwords", quiet=True)

from nltk.corpus import stopwords

# Function for removing particular parts of sentences using regex
def pre_processing(sentences):
    clean_sentences = pd.Series(sentences)

    # make alphabets lowercase
    clean_sentences = [s.lower() for s in clean_sentences]

    dir_remove = lambda sen: re.sub("\#[0-9]+ from (\/)?[a-zA-Z0-9]+\/([a-zA-Z0-9]+(\/)?)*", " ", sen)
    clean_sentences = [dir_remove(i) for i in clean_sentences]

    return clean_sentences

def run_summarization(df, type):

    text = []

    # Reading from the dataframe
    for i in range(0, 300):
        li = df.iloc[i][type]
        if li == 'Nan':
            continue
        li = li.replace('\n', ' ')
        text.append(li)

    text = pre_processing(text)

    # Running LSA Summarizer
    summarizer = LsaSummarizer()
    stopWords = stopwords.words('english')
    summarizer.stop_words = stopWords
    summary = summarizer(text, 20)

    # Joining the output summary sentences and storing in a variable
    summ = "\n".join(summary)

    # T5 Model Summarizer (Abstractive Summarization)
    model = T5ForConditionalGeneration.from_pretrained('t5-small')
    tokenizer = T5Tokenizer.from_pretrained('t5-small')
    device = torch.device('cpu')

    preprocess_text = summ.strip().replace("\n","")
    t5_prepared_Text = "summarize: "+preprocess_text

    tokenized_text = tokenizer.encode(t5_prepared_Text, return_tensors="pt", max_length=512, truncation=True).to(device)

    summary_ids = model.generate(tokenized_text, num_beams=4, no_repeat_ngram_size=2, min_length=30, max_length=1000, early_stopping=True)

    output = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

    return output





