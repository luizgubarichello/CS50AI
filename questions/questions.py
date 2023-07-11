import nltk
import sys
import os
import string
import math

FILE_MATCHES = 1
SENTENCE_MATCHES = 1

nltk.download("stopwords")
nltk.download("punkt")

def main():
    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {filename: tokenize(files[filename]) for filename in files}
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    file_dict = dict()
    file_list = os.listdir(directory)
    for file in file_list:
        file_path = f"{directory}{os.sep}{file}"
        with open(file_path) as f:
            file_dict[file] = f.read()
    return file_dict


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    stopwords = nltk.corpus.stopwords.words("english")
    punctuation = string.punctuation
    words = [
        word
        for word in nltk.word_tokenize(document.lower())
        if word not in stopwords and not all(char in punctuation for char in word)
    ]
    return words


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    words = set()
    for document in documents:
        words.update(documents[document])

    idfs = dict()
    for word in words:
        f = sum(word in documents[document] for document in documents)
        idf = math.log(len(documents) / f)
        idfs[word] = idf
    
    return idfs


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    file_score = dict()
    for filename in files:
        file_score[filename] = 0
        for word in query:
            if word in files[filename]:
                tf = files[filename].count(word)
                tfidf = tf * idfs[word]
                file_score[filename] += tfidf
            else:
                continue

    sorted_scores = sorted(file_score, key=lambda k: file_score[k], reverse=True)
    top_files_list = sorted_scores[:n]

    return top_files_list


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    sentence_score = dict()
    for sentence in sentences:
        sentence_score[sentence] = {
            'score': 0,
            't_d': 0,
        }
        for word in query:
            if word in sentences[sentence]:
                sentence_score[sentence]['score'] += idfs[word]
                sentence_score[sentence]['t_d'] += 1
            else:
                continue
        sentence_score[sentence]['t_d'] /= len(sentences[sentence])
    
    sorted_items = sorted(sentence_score.items(), key=lambda x: (x[1]['score'], x[1]['t_d']), reverse=True)
    top_sentences_list = [s_item[0] for s_item in sorted_items[:n]]

    return top_sentences_list


if __name__ == "__main__":
    main()
