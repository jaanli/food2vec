"""Preprocess data from ../dat/RecipesScraper tool."""
import re
import json
import util
import os


def load_ingredients_lists(path):
  with open(path, 'r') as f:
    data_dict = json.loads(f.read())
    recipe_list = data_dict['recipes']
    res = [recipe['ingredients'] for recipe in recipe_list]
    res = [x for x in res if len(x) > 0]
    res = list(filter(lambda x: not x[-1].lower().startswith('equ'), res))
    alphanum = lambda x: re.sub("[^a-zA-Z]", " ", x).strip().lower()
    res = [list(map(alphanum, l)) for l in res]
    flatten = lambda l: [item for sublist in l for item in sublist]
    res = [flatten([w.split() for w in l]) for l in res]
    return [l for l in res if len(l) >= 2]


def parse_scraped_site(in_path, out_path):
  """load vocab fit to nature and kaggle data
  from
  http://www.nature.com/articles/srep00196wget
  https://www.kaggle.com/c/whats-cooking/download/train.json.zip
  and match it to scraped allrecipes data
  """
  vocab = util.load_vocab('../fit/nature_and_kaggle_vocab.txt')
  foods = [tup[0] for tup in vocab]
  ingredients_lists = load_ingredients_lists(in_path)
  # ingredients_lists = ingredients_lists[0:1000]  # for debugging
  ingredients_lists = [util.filter_stopwords(l) for l in ingredients_lists]
  parsed_ingredients = util.parse_ingredients_parallel(foods, ingredients_lists)
  parsed_recipes = [("Unknown", ingredients) for \
      ingredients in parsed_ingredients]
  util.write_recipes(parsed_recipes, out_path)


def main():
  for root, dirname, filenames in os.walk('./RecipesScraper/output'):
    for filename in filenames:
      name, ext = os.path.splitext(filename)
      out_path = os.path.join('./processed', name + '.csv')
      if not os.path.exists(out_path):
        parse_scraped_site(
            in_path=os.path.join(root, filename),
            out_path=out_path)


if __name__ == '__main__':
  main()
