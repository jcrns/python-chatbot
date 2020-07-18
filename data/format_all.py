    
import random
import sys
import nltk
import itertools
from collections import defaultdict
import numpy as np
import pickle

# Creating whitelist and blacklist characters
EN_WHITELIST = '0123456789abcdefghijklmnopqrstuvwxyz ' # space is included in whitelist
EN_BLACKLIST = '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~\''

# Filename of text we will format
filenames = ['formatted_movie_lines.txt']

# Defining limits
limit = {
        # Max len of string
        'maxq' : 20,
        'minq' : 0,
        'maxa' : 20,
        'mina' : 3
        }

UNK = 'unk'

# Number of words the chatbot will use
VOCAB_SIZE = 100000

# Spliting dataset
def split_dataset(x, y, ratio = [0.7, 0.15, 0.15] ):
    # number of examples
    data_len = len(x)
    lens = [ int(data_len*item) for item in ratio ]

    trainX, trainY = x[:lens[0]], y[:lens[0]]
    testX, testY = x[lens[0]:lens[0]+lens[1]], y[lens[0]:lens[0]+lens[1]]
    validX, validY = x[-lens[-1]:], y[-lens[-1]:]

    return (trainX,trainY), (testX,testY), (validX,validY)

# Replacing words with indices in a sequence and replacing with unknown if word not in lookup
def pad_seq(seq, lookup, maxlen):
    indices = []

    # Looping through list of words and checking if the words
    for word in seq:
        if word in lookup:
            indices.append(lookup[word])
        else:
            indices.append(lookup[UNK])

    # Appending word to list 
    # indices.append(lookup[word])
    
    return indices + [0]*(maxlen - len(seq))


# Creating function that opens file and spliting by line breaks
def read_lines(filename):
    return open(filename).read().split('\n')[:-1]

# Function removing whitelisted characters
def filter_line(line, whitelist):
    return ''.join([ ch for ch in line if ch in whitelist ])

# Function to filterout certain strings
def filter_data(sequences):
    filtered_q, filtered_a = [], []
    raw_data_len = len(sequences)//2

    # Checking in for loop if formatted string is too short or long else appending
    for i in range(0, len(sequences), 2):
        try:
            # Indexing statement and response
            qlen, alen = len(sequences[i].split(' ')), len(sequences[i+1].split(' '))

            # Checking if the length of statement is on par
            if qlen >= limit['minq'] and qlen <= limit['maxq']:

                # Checking if the length of response is on par
                if alen >= limit['mina'] and alen <= limit['maxa']:

                    # Appending statement to list
                    filtered_q.append(sequences[i])

                    # Appending comment to list
                    filtered_a.append(sequences[i+1])
        except Exception as e:
            print(e)
            continue
        
    # Checking how much of the original data is filtered
    filt_data_len = len(filtered_q)
    filtered = int((raw_data_len - filt_data_len)*100/raw_data_len)
    print(str(filtered) + '% filtered from original data')

    return filtered_q, filtered_a

# Creating function indexing sentences
def index_(tokenized_sentences, vocab_size):

    # get frequency distribution
    freq_dist = nltk.FreqDist(itertools.chain(*tokenized_sentences))
    
    print(freq_dist)
    print("freq_dist")

    # get vocabulary of 'vocab_size' most used words
    vocab = freq_dist.most_common(vocab_size)
    
    print(vocab)
    print("vocab")

    # index2word
    index2word = ['_'] + [UNK] + [ x[0] for x in vocab ]
    # index2word = [ x[0] for x in vocab ]
    
    print(index2word)
    print("index2word")

    # word2index Adding id number to each word
    word2index = dict([(w,i) for i,w in enumerate(index2word)] )
    
    print(word2index)
    print("word2index")
    
    return index2word, word2index, freq_dist

# 
def zero_pad(qtokenized, atokenized, w2idx):
    # num of rows
    data_len = len(qtokenized)

    # numpy arrays to store indices
    idx_q = np.zeros([data_len, limit['maxq']], dtype=np.int32)
    idx_a = np.zeros([data_len, limit['maxa']], dtype=np.int32)

    for i in range(data_len):
        q_indices = pad_seq(qtokenized[i], w2idx, limit['maxq'])
        a_indices = pad_seq(atokenized[i], w2idx, limit['maxa'])

        #print(len(idx_q[i]), len(q_indices))
        #print(len(idx_a[i]), len(a_indices))
        idx_q[i] = np.array(q_indices)
        idx_a[i] = np.array(a_indices)

    return idx_q, idx_a

# Creating function which will make needed files for training 
def process_data():
    
    print('\n>> Read lines from file')
    for filename in filenames:
        lines = read_lines(filename=filename)

    # change to lower case (just for en)
    lines = [ line.lower() for line in lines ]

    print('\n:: Sample from read(p) lines')
    print(lines[121:125])

    # filter out unnecessary characters
    print('\n>> Filter lines')
    lines = [ filter_line(line, EN_WHITELIST) for line in lines ]
    print(lines[121:125])

    # filter out too long or too short sequences
    print('\n>> 2nd layer of filtering')
    qlines, alines = filter_data(lines)
    print('\nq : {0} ; a : {1}'.format(qlines[60], alines[60]))
    print('\nq : {0} ; a : {1}'.format(qlines[61], alines[61]))


    # convert list of [lines of text] into list of [list of words ]
    print('\n>> Segment lines into words')
    qtokenized = [ wordlist.split(' ') for wordlist in qlines ]
    atokenized = [ wordlist.split(' ') for wordlist in alines ]
    print('\n:: Sample from segmented list of words')
    print('\nq : {0} ; a : {1}'.format(qtokenized[60], atokenized[60]))
    print('\nq : {0} ; a : {1}'.format(qtokenized[61], atokenized[61]))


    # indexing -> idx2w, w2idx : en/ta || Indexing all words
    print('\n >> Index words')
    print('indexing words')
    print(len(qtokenized))
    print(len(alines))
    idx2w, w2idx, freq_dist = index_( qtokenized + atokenized, vocab_size=VOCAB_SIZE)

    print('\n >> Zero Padding')
    idx_q, idx_a = zero_pad(qtokenized, atokenized, w2idx)

    print('\n >> Save numpy arrays to disk')
    # save them
    np.save('idx_q.npy', idx_q)
    np.save('idx_a.npy', idx_a)

    # let us now save the necessary dictionaries
    metadata = {
            'w2idx' : w2idx,
            'idx2w' : idx2w,
            'limit' : limit,
            'freq_dist' : freq_dist
                }

    # write to disk : data control dictionaries
    with open('metadata.pkl', 'wb') as f:
        pickle.dump(metadata, f)

# Function for loading data
def load_data(PATH=''):

    # Trying to get local metadata
    try:
        with open(PATH + 'metadata.pkl', 'rb') as f:
            metadata = pickle.load(f)
    except:
        metadata = None

    # read numpy arrays
    idx_q = np.load(PATH + 'idx_q.npy')
    idx_a = np.load(PATH + 'idx_a.npy')
    return metadata, idx_q, idx_a


# If file is ran we are creating formatted training files from text file
if __name__ == '__main__':
    process_data()
