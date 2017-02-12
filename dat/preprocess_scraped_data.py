"""Preprocess data from ../dat/RecipesScraper tool."""
import re
import json
import util


def load_ingredients_lists(path):
  with open(path, 'r') as f:
    raw = f.readlines()
    string = "[" + ",".join(raw) + "]"
    recipe_list = json.loads(string)
    res = [recipe['ingredients'][:-2] for recipe in recipe_list]
    alphanum = lambda x: re.sub("[^a-zA-Z]", " ", x).strip().lower()
    res = [list(map(alphanum, l)) for l in res]
    flatten = lambda l: [item for sublist in l for item in sublist]
    res = [flatten([w.split() for w in l]) for l in res]
    return [l for l in res if len(l) >= 2]


def parse_scraped_site(json_path, out_path):
  """load vocab fit to nature and kaggle data
  from
  http://www.nature.com/articles/srep00196wget
  https://www.kaggle.com/c/whats-cooking/download/train.json.zip
  and match it to scraped allrecipes data
  """
  vocab = util.load_vocab('../fit/nature_and_kaggle_vocab.txt')
  foods = [tup[0] for tup in vocab]
  ingredients_lists = load_ingredients_lists(json_path)
  # ingredients_lists = ingredients_lists[0:1000]  # for debugging
  ingredients_lists = [util.filter_stopwords(l) for l in ingredients_lists]
  print(ingredients_lists[0])
  parsed_ingredients = util.parse_ingredients_parallel(foods, ingredients_lists)
  parsed_recipes = [("Unknown", ingredients) for \
      ingredients in parsed_ingredients]
  util.write_recipes(parsed_recipes, out_path)


def main():
  parse_scraped_site(
      json_path='./RecipesScraper/output/allrecipes_recipes.json',
      out_path='allrecipes_recipes.csv')
  parse_scraped_site(
      json_path='./RecipesScraper/output/jamieoliver_recipes.json',
      out_path='jamieoliver_recipes.csv')


if __name__ == '__main__':
  main()
