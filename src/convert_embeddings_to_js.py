import h5py
import json
import numpy as np

def load_embeddings(path):
  f = h5py.File(path, 'r')
  nemb = f['nemb'][:]
  f.close()
  return nemb

def load_vocab(path):
  vocab = []
  with open(path, 'rb') as f:
    for line in f.readlines():
      split = line.split(' ')
      vocab.append((split[0], int(split[1].rstrip())))
  # ignore UNK at position 0
  return vocab[1:]

def write_to_js(words, embeddings, path):
  word_vecs = {}
  for word, embedding in zip(words, embeddings):
    word_vecs[word] = embedding.tolist()
  with open(path, 'wb') as f:
    json.dump(word_vecs, f)
    f.write(';')



def main():
  nemb = load_embeddings(path='/tmp/embeddings.h5')
  vocab = load_vocab('/tmp/vocab.txt')
  words = [tup[0] for tup in vocab]
  # dont use UNK
  words = words[1:]
  nemb = nemb[1:]
  # lower precision, faster
  nemb = nemb.astype(np.float16)
  write_to_js(words, nemb[1:], path='../../word2vecjson/data/foodVecs.js')

if __name__ == '__main__':
  main()
