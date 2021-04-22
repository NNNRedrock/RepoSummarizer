from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals
import math
import numpy
import nltk

from warnings import warn
from nltk.tokenize import sent_tokenize, word_tokenize
from numpy.linalg import svd as singular_value_decomposition
from repo_sum.base_summarizer import BaseSummarizer
from nltk.corpus import stopwords

class LsaSummarizer(BaseSummarizer):
    MIN_DIMENSIONS = 3
    REDUCTION_RATIO = 1/1

    _stop_words = list(stopwords.words('english'))

    @property
    def stop_words(self):
        return self._stop_words

    @stop_words.setter
    def stop_words(self, words):
        self._stop_words = words

    def __call__(self, document, sentences_count):

        dictionary = self._create_dictionary(document)
        
        if not dictionary:
            return ()

        sentences = []
        # Running a loop to separate out the sentences in the document and storing in a list
        for i in range(0, len(document)):
            li = sent_tokenize(document[i])
            sentences.extend(li)

        matrix = self._create_matrix(document, dictionary)
        matrix = self._compute_term_frequency(matrix)
        u, sigma, v = singular_value_decomposition(matrix, full_matrices=False)

        ranks = iter(self._compute_ranks(sigma, v))
        return self._get_best_sentences(sentences, sentences_count,
            lambda s: next(ranks))

    # Function for creating a dictionary of words
    def _create_dictionary(self, document):

        words = []
        for i in range(0, len(document)):
            li = word_tokenize(document[i])
            words.extend(li)
        words = tuple(words)

        # Converting words into lower case
        words = map(self.normalize_word, words)

        # Filtering the stopwords
        unique_words = frozenset(w for w in words if w not in self._stop_words)

        return dict((w, i) for i, w in enumerate(unique_words))

    def _create_matrix(self, document, dictionary):
        sentences = []
        for i in range(0, len(document)):
            li = sent_tokenize(document[i])
            sentences.extend(li)

        words_count = len(dictionary)
        sentences_count = len(sentences)
        # Words count should be greater than sentance count for good summarization output
        if words_count < sentences_count:
            message = (
                "Number of words (%d) is lower than number of sentences (%d). "
                "LSA algorithm may not work properly."
            )
            warn(message % (words_count, sentences_count))

        # Creating a matrix of dimension (words_count * sentences_count)
        matrix = numpy.zeros((words_count, sentences_count))
        for col, sentence in enumerate(sentences):
            words = word_tokenize(sentence)
            for word in words:
                # only valid words is counted (not stop-words, ...)
                if word in dictionary:
                    row = dictionary[word]
                    matrix[row, col] += 1

        return matrix

    def _compute_term_frequency(self, matrix, smooth=0.4):

        assert 0.0 <= smooth < 1.0

        max_word_frequencies = numpy.max(matrix, axis=0)
        rows, cols = matrix.shape
        for row in range(rows):
            for col in range(cols):
                max_word_frequency = max_word_frequencies[col]
                if max_word_frequency != 0:
                    frequency = matrix[row, col]/max_word_frequency
                    matrix[row, col] = smooth + (1.0 - smooth)*frequency

        return matrix

    # Function for computing ranks for the sentences
    def _compute_ranks(self, sigma, v_matrix):
        assert len(sigma) == v_matrix.shape[0]

        dimensions = max(LsaSummarizer.MIN_DIMENSIONS,
            int(len(sigma)*LsaSummarizer.REDUCTION_RATIO))
        powered_sigma = tuple(s**2 if i < dimensions else 0.0
            for i, s in enumerate(sigma))

        ranks = []
        
        for column_vector in v_matrix.T:
            rank = sum(s*v**2 for s, v in zip(powered_sigma, column_vector))
            ranks.append(math.sqrt(rank))

        return ranks
