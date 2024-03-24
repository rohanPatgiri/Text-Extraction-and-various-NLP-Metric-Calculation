import os
import pandas as pd
import re
from nltk.corpus import stopwords
from textblob import TextBlob

# Load stop words from the text files in the Stopwords folder
stop_words = []
stop_words_files = ['StopWords/StopWords_Auditor.txt', 'StopWords/StopWords_Currencies.txt', 'StopWords/StopWords_DatesandNumbers.txt', 'StopWords/StopWords_Generic.txt', 'StopWords/StopWords_GenericLong.txt', 'StopWords/StopWords_Geographic.txt', 'StopWords/StopWords_Names.txt']
for file in stop_words_files:
    with open(file, 'r') as f:
        stop_words.extend(f.read().splitlines())

# Load positive and negative words
with open('MasterDictionary/negative-words.txt', 'r') as f:
    negative_words = set(f.read().splitlines())
with open('MasterDictionary/positive-words.txt', 'r') as f:
    positive_words = set(f.read().splitlines())

# Read input file
df = pd.read_excel('Input.xlsx')

# Initialize result dataframe
result = pd.DataFrame(columns=['URL_ID', 'URL', 'Positive Score', 'Negative Score', 'Polarity Score', 'Subjectivity Score', 'Avg Sentence Length', 'Percentage of Complex Words', 'Fog Index', 'Avg Number of Words per Sentence', 'Complex Word Count', 'Word Count', 'Syllable per Word', 'Personal Pronouns', 'Avg Word Length'])

# Function to count the number of syllables. This function is used to calculate the "complex_world" variable.
def syllable_count(word):
    word = word.lower()
    count = 0
    vowels = "aeiouy"
    if word[0] in vowels:
        count += 1
    for index in range(1, len(word)):
        if word[index] in vowels and word[index - 1] not in vowels:
            count += 1
    if word.endswith("es") or word.endswith("ed"):
        # subtract 1 if the word ends with "es" or "ed" but not if the letter before is a vowel
        if len(word) > 2 and word[-3] not in vowels:
            count -= 1
    return count

# Analyze each text file
for index, row in df.iterrows():
    with open(os.path.join('extracted_text', f'{row["URL_ID"]}.txt'), 'r', encoding='utf-8') as f:
        text = f.read()
        words = [word for word in text.split() if word not in stop_words]
        sentences = text.split('.')
        if len(words) == 0:
            continue
        # the 13 lines below calculates the 13 variables as required by the assignment
        positive_score = len([word for word in words if word in positive_words])
        negative_score = len([word for word in words if word in negative_words])
        polarity_score = TextBlob(text).sentiment.polarity
        subjectivity_score = TextBlob(text).sentiment.subjectivity
        avg_sentence_length = len(words) / len(sentences)
        complex_words = [word for word in words if syllable_count(word) > 2]
        percentage_complex_words = len(complex_words) / len(words)
        fog_index = 0.4 * (avg_sentence_length + percentage_complex_words)
        complex_word_count = len(complex_words)
        word_count = len(words)
        syllable_per_word = sum(syllable_count(word) for word in words) / len(words)
        personal_pronouns = len(re.findall(r'\bI\b|\bwe\b|\bmy\b|\bours\b|\bus\b', text, re.IGNORECASE))
        avg_word_length = sum(len(word) for word in words) / len(words)
        
        # Here, a new Pandas Dataframe row is created where the 13 above variables that wrere calculatec above are stored. 
        new_row = pd.DataFrame({'URL_ID': [row['URL_ID']], 'URL': [row['URL']], 'Positive Score': [positive_score], 'Negative Score': [negative_score], 'Polarity Score': [polarity_score], 'Subjectivity Score': [subjectivity_score], 'Avg Sentence Length': [avg_sentence_length], 'Percentage of Complex Words': [percentage_complex_words], 'Fog Index': [fog_index], 'Avg Number of Words per Sentence': [len(words) / len(sentences)], 'Complex Word Count': [complex_word_count], 'Word Count': [word_count], 'Syllable per Word': [syllable_per_word], 'Personal Pronouns': [personal_pronouns], 'Avg Word Length': [avg_word_length]})
        # Next, that row is concatenated with the "result" Pandas dataframe that was created above
        result = pd.concat([result, new_row], ignore_index=True)

# Write result to output file
result.to_excel('Output.xlsx', index=False)
