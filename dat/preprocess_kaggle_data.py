import os
import json
import itertools
import re
from tqdm import tqdm

def load_vocab(path):
  vocab = []
  with open(path, 'rb') as f:
      for line in f.readlines():
          split = line.split(' ')
          vocab.append((split[0], int(split[1].rstrip())))
  # ignore UNK at position 0
  return vocab[1:]


def load_recipes(path):
  with open(path, 'rb') as f:
    data = json.load(f)
  decode_list = lambda l: [x.encode('ascii', 'ignore') for x in l]
  recipes = [(item['cuisine'].encode('ascii', 'ignore'), decode_list(item['ingredients'])) for item in data]
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


def lookup_ingredient(vocab, ingredient):
  if ingredient in vocab:
    return ingredient
  else:
    split = ingredient.lower().replace('-', ' ').replace('%', '').split(' ')
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


def get_country2region():
  return {'irish': 'WesternEuropean',
      'mexican': 'LatinAmerican',
      'filipino': 'SoutheastAsian',
      'vietnamese': 'SoutheastAsian',
      'moroccan': 'African',
      'brazilian': 'LatinAmerican',
      'japanese': 'EastAsian',
      'british': 'WesternEuropean',
      'greek': 'SouthernEuropean',
      'indian': 'SouthAsian',
      'jamaican': 'LatinAmerican',
      'french': 'WesternEuropean',
      'spanish': 'SouthernEuropean',
      'russian': 'NorthernEuropean',
      'cajun_creole': 'LatinAmerican',
      'thai': 'SoutheastAsian',
      'southern_us': 'NorthAmerican',
      'korean': 'EastAsian',
      'chinese': 'EastAsian',
      'italian': 'SouthernEuropean'}


def write_recipes(recipes, path):
  with open(path, 'wb') as f:
    for tup in recipes:
      f.write(','.join([tup[0]] + tup[1]).lstrip().rstrip() + '\n')


def main():
  path = '/Users/jaanaltosaar/fit/food2vec/2017-01-20/'
  vocab = load_vocab(os.path.join(path, 'vocab.txt'))
  foods = [tup[0] for tup in vocab]
  recipes = load_recipes('./train.json')
  cuisines = set([tup[0] for tup in recipes])
  country2region = get_country2region()
  parsed_recipes = parse_recipes(foods, country2region, recipes)
  write_recipes(parsed_recipes, 'kaggle_recipes.csv')


if __name__ == '__main__':
  main()
