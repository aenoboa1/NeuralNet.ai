import numpy as np
import random as rnd


class Dataset:
    def __init__(self,fname='' ,source='stanford'):
        self.fname = fname # The file name variable
        self.source = source
        self.dataset = self.ReadDataset()
        self.vocabulary ,self.vocabulary_size = self.get_vocabulary()
        self.word_map = self.get_mappings()
        self.word_counts = self.get_word_counts()
        self.size = len(self.dataset)
        self.aug_ds = self.DataAugmentation()

    # data augmentation for words
    # using probability
    # frequency of given words

    def DataAugmentation(self,threshold=1e-5,N=30,min_length=3):
        print("Applying data augmentation")
        n_words = 0
        for word in self.word_counts:
            # increment for the key in the dict
            n_words += self.word_counts[word]

        # We don't need double precision (f64)
        reject_P = np.zeros(self.vocabulary_size,dtype=np.float32)

        for idx,word in enumerate(self.vocabulary):
            frequency = ( self.word_counts[word])/(n_words)
            reject_P[idx] = max(0,1-np.sqrt(threshold/frequency))

        all_sentences = []
        # Iterate over N times
        #If greater prob than random
        for sentence in self.dataset * N:
            new_sentences = []
            for word in sentence:
                if reject_P[self.word_map[word]] == 0 \
                        or rnd.random() >= reject_P[self.word_map[word]]:
                            new_sentences.append(word)
            if len(new_sentences) >= min_length:
                all_sentences.append(new_sentences)

        print("The len of the new sentences is ", len(all_sentences))
        return all_sentences

    @property
    def __len__(self) -> int:
        return self.dataset.__len__()

    def ReadDataset(self) -> list:
        print("Converting the file to dataset format")
        sentences = []
        reviews = open(self.fname).readlines()
        len_reviews = len(reviews)
        first = self.source == 'stanford'
        offset = int(first)
        # iterate over lines
        for line in range(len_reviews):
            if first:
                first=False
                continue
            # seperated by a space
            sentence = [w.lower() for w in reviews[line].split()[offset:]]
            sentences.append(sentence)
        print(f"Compiled list of sentences in the dataset: {len(sentences)} sentences")
        return sentences

    def get_random_context():
        """


        """

        return rnd.random(),np.zeros(3)




    def get_vocabulary(self):
        print("Tabbing vocabulary")
        vocabulary = []
        for sentence in self.dataset:
            for word in sentence:
                if word not in vocabulary:
                    vocabulary.append(word)

        vocabulary_size = len(vocabulary)
        print(f" found {vocabulary_size} distinct words")
        return vocabulary,vocabulary_size

    def get_mappings(self) :
        print("Mapping word to int index...")
        mapping = {}
        idx = 0
        for word in self.vocabulary:
            if word not in mapping:
                mapping[word] = idx
                idx += 1
        return mapping

    def get_word_counts(self) -> dict:
        print("Getting word counts...")
        word_cnt = {}
        for word in self.vocabulary:
            word_cnt[word] = 0

        for sentence in self.dataset:
            for word in sentence:
                word_cnt[word] += 1
        return word_cnt
