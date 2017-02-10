import os
import json
import itertools
import re
import joblib
from tqdm import tqdm
from nltk.corpus import stopwords


def load_vocab(path):
  vocab = []
  with open(path, 'r') as f:
      for line in f.readlines():
          split = line.split(' ')
          vocab.append((split[0], int(split[1].rstrip())))
  # ignore UNK at position 0
  return vocab[1:]


def load_recipes(path):
  with open(path, 'r') as f:
    data = json.load(f)
  enc = lambda x: x.encode('ascii', 'ignore')
  recipes = [(enc(item['cuisine']), list(map(enc, item['ingredients']))) for item in data]
  to_str = lambda x: x.decode('utf-8', 'ignore')
  recipes = [(to_str(item[0]), list(map(to_str, item[1]))) for item in recipes]
  return recipes


def parse_recipes(vocab, country2region, recipes):
  parsed_recipes = []
  for i in tqdm(range(len(recipes))):
    cuisine, ingredients = recipes[i]
    lookup = []
    for ingredient in ingredients:
      lookup.append(lookup_ingredient(vocab, ingredient))
    if len(lookup) >= 2:
      parsed_recipes.append((country2region[cuisine], lookup))
  return parsed_recipes


def parse_recipe(vocab, country2region, recipe):
  cuisine, ingredients = recipe
  mapped = [lookup_ingredient(vocab, ingredient) for ingredient in ingredients]
  if len(mapped) >=2:
    return (country2region[cuisine], mapped)


def parse_recipes_parallel(vocab, country2region, recipes):
  parsed = joblib.Parallel(n_jobs=8, verbose=50)(
      joblib.delayed(parse_recipe)(
        vocab, country2region, recipe) for recipe in recipes)
  return [item for item in parsed if item is not None]


def parse_ingredients(vocab, ingredients):
  mapped = [lookup_ingredient(vocab, ingredient) for ingredient in ingredients]
  if len(mapped) >= 2:
    return mapped


def parse_ingredients_parallel(vocab, ingredients_lists):
  parsed = joblib.Parallel(n_jobs=8, verbose=50)(
      joblib.delayed(parse_ingredients)(
        vocab, ingredients) for ingredients in ingredients_lists)
  return [item for item in parsed if item is not None]


def lookup_ingredient(vocab, ingredient):
  if ingredient in vocab:
    return ingredient
  else:
    split = ingredient.lower().replace('-', ' ').replace('%', '').split(' ')
    # remove non-alphanumeric characters like é
    split = [re.sub(r'([^\s\w]|_)+', '', x) for x in split]
    if len(split) == 1:
      return split[0]
    else:
      full = []
      for i in range(1, len(split)):
        for permutation in itertools.permutations(split, i):
          full.append('_'.join(permutation))
      match = next((perm for perm in full if perm in vocab), None)
      if match is not None:
        return match
      else:
        return '_'.join(split)


def write_recipes(recipes, path):
  with open(path, 'w') as f:
    for tup in recipes:
      f.write(','.join([tup[0]] + tup[1]).lstrip().rstrip() + '\n')


def filter_stopwords(lst):
  blacklist = ['cup', 'teaspoon', 'cups', 'ounce', 'chopped', 'tablespoons', 'ground', 'and', 'to', 'taste', 'fresh', 'teaspoons', 'or', 'can', 'sliced', 'powder', 'pound', 'all', 'package', 'minced', 'diced', 'into', 'chunks', 'cup', 'dry', 'uncooked', 'peeled', 'and', 'the', 'in', 'cubes', 'inch', 'to', 'taste', 'chopped', 'cups', 'teaspoon', 'tsp', 'tablespoon', 'tbsp', 'quart', 'sliced', 'into', 'torn', 'stemmed', 'minced', 'cracked', 'rings', 'whole', 'strips', 'bunch', 'sprigs', 'fresh', 'cut', 'pinch', 'pound', 'finely', 'seeded', 'as', 'needed', 'need', 'chunks', 'juiced','soaked', 'soak', 'overnight', 'low', 'optional', 'piece', 'head', 'large', 'small', 'cored', 'medium', 'such', 'cover', 'pitted', 'halved', 'quartered', 'package', 'packages', 'grated','separated', 'florets', 'softened', 'half', 'medium', 'freshly', 'of', 'halves', 'beaten', 'cooked', 'leaves', 'needed', 'pieces', 'crushed', 'extra', 'pitted', 'flavored', 'unsweetened', 'prepared', 'light', 'jar', 'paste', 'chunks', 'quartered', 'seasoned', 'sweetened', 'thin', 'flaked', 'rolled', 'canned', 'mashed', 'garnish', 'french', 'evaporated', 'liquid', 'lengthwise', 'sifted', 'wedges', 'puree', 'pure', 'pint', 'quarts', 'squares', 'undrained', 'chilled', 'raw', 'separated', 'c', 'zested', 'hard', 'frozen', 'drained', 'rinsed', 'squeezed', 'welfare', 'x', 'g', 'ml', 'sticks', 'higher', 'spatchcocked', 'free', 'range', 'bite', 'sized']
  stop = set(stopwords.words('english') + blacklist)
  res = []
  for word in lst:
    if word not in stop:
      res.append(word)
  return res
