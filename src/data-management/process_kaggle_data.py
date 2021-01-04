"""Preprocess training data from
https://www.kaggle.com/c/whats-cooking/download/train.json.zip
"""
import util


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


def main():
  # load vocab fit to http://www.nature.com/articles/srep00196wget
  vocab = util.load_vocab('../fit/nature_and_kaggle_vocab.txt')
  foods = [tup[0] for tup in vocab]
  recipes = util.load_recipes('../dat/train.json')
  recipes = [recipe for recipe in recipes if len(recipe[1]) < 30]
  # recipes = recipes[0:1000]  # debug on smaller dataset
  country2region = get_country2region()
  # match the kaggle data to the nature data vocabulary
  # parsed_recipes = util.parse_recipes(foods, country2region, recipes)
  parsed_recipes = util.parse_recipes_parallel(foods, country2region, recipes)
  util.write_recipes(parsed_recipes, 'kaggle_recipes.csv')


if __name__ == '__main__':
  main()
