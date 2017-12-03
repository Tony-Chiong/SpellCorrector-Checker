#!/usr/bin/env python

import numpy
import sys
import operator
import time


def suggest_words(root, target, max_distance):
    suggestions = []
    find_editdistances(root, target, 1, [0], suggestions, max_distance)
    return suggestions

def find_editdistances(root, target, currentrow_num, lastrow, distances, max_distance): 
    """ Traverses trie and calculates edit distances of every word in dictionary to the
        target word.  It does not keep the whole edit distance matrix in memory.
        Only the last row and current row are needed because we are incremently building
        up the distance matrix based on word prefixes obtained from the trie.
    """

    alphabet = root.alphabet

    # Prune search space to make more efficient.
    # If a entry in the edit distance row is greater
    # than max_distance we no longer need finish calculating
    # the rest of the words edit distance.
    if min(lastrow) > max_distance:
        return

    # e.g list(dict.items())
    # e.g list(alphabet.items())

    # for candidate_char, trie in alphabet.iteritems():
    for candidate_char, trie in alphabet.items():
          # create first row of edit distance matrix only if
          # we are in the first recursive call
          if currentrow_num == 1:
              lastrow = [i for i in range(len(target)+1)]

          # calculate edit distance for the current letter.
          row = [currentrow_num]
          for i, target_char in enumerate(target, start=1):
              if target_char == candidate_char:
                  row.append(lastrow[i-1])
              else:
                  row.append(min(lastrow[i-1]+1,
                             lastrow[i]+1,
                             row[i-1]+1))

          edit_distance = row[-1]
          if trie.endpoint and edit_distance <= max_distance:
              distances.append(trie.endpoint)

          find_editdistances(trie, target, currentrow_num+1, row, distances, max_distance)
  


def create_triedict(word_src):
    """Creates a trie from all the words in the Unix dictionary """

    trie = Trie()
    with open(word_src, 'rt') as f:
        for word in f.read().split():
            trie.insert(word.lower())
    return trie

def levenshtein(source,target):

    """First implementation of Levenshtein Distance.
       Not used in trie base version
    """

    slen = len(source)+1
    tlen = len(target)+1
    m = numpy.zeros((tlen, slen))

    # change to using normal lists
    for j in range(1,tlen):
        m[j,0] = j

    for i in range(1,slen):
        m[0,i] = i

    for j, tlet in enumerate(target, start=1):
        for i,slet in enumerate(source, start=1):
            if tlet == slet:
                m[j, i] = m[j-1,i-1]
            else:
                m[j, i] = min(m[j-1,i-1]+1,
                             m[j-1,i]+1,
                             m[j,i-1]+1)

    return m[tlen-1, slen-1]

class Trie:
    """Trie consists of a dictionary of letters -> trie nodes """

    def __init__(self):
      self.alphabet = {}
      self.endpoint = None

    def insert(self, word):
      current = self
      for char in word:
        if char not in current.alphabet:
          current.alphabet[char] = Trie()
        current = current.alphabet[char]
      current.endpoint = word

    def print_trie(self, alphabet,n):
      """Print the trie data structure in a somewhat readable format """

      for k,v in alphabet.items():
        for i in range(n): print(' '),
        print(k)
        if v.endpoint:
          pass
        self.print_trie(v.alphabet, n+1)

    def find(self, word):
        """Checks to see if a word exists in the trie """

        current = self
        for char in word:
          if char not in current.alphabet:
              return False
          current = current.alphabet[char]
        if current.endpoint == word:
            return True
        return False


def read_dic(word_src):
    words, freqs = [], []
    with open(word_src, 'rt') as f:
        for idx, word in enumerate(f.read().split()):
            if idx % 2 == 0:
                words.append(word.lower())
            else:
                freqs.append(int(word))
    dic = dict()
    for idx, ele in enumerate(words):
        dic[ele] = freqs[idx]
    return dic


def dic_sort(dic):
    dic_sort_by_value = sorted(dic.items(), key=operator.itemgetter(1), reverse=True)
    dic_sort_by_key = sorted(dic.items(), key=operator.itemgetter(0), reverse=True)
    return dic_sort_by_value, dic_sort_by_key


if __name__ == '__main__':
    # word_src = sys.argv[1]
    # word = sys.argv[2]
    # max_dist = int(sys.argv[3])
    # t = create_triedict(word_src)
    # suggestions = suggest_words(t, word, max_dist)
    # print(suggestions)

    t0 = time.time()

    word_src = 'my_word_freq.txt'
    word = 'a_cover_plastia'
    max_dist = 5
    t = create_triedict(word_src)
    suggestions = suggest_words(t, word, max_dist)

    dic = read_dic(word_src)
    print(dic)
    dic_sug = dict()
    for idx, suggestion in enumerate(suggestions):
        dic_sug[suggestion] = dic[suggestion]
    print(dic_sug)
    dic_sug_sort = dic_sort(dic_sug)[0]
    print(dic_sug_sort)

    for idx, suggestion in enumerate(dic_sug_sort):
        print(f'idx = {idx}, suggestion = {suggestion}')

    print(f'overall computing time: {time.time()-t0:.8f} s')
