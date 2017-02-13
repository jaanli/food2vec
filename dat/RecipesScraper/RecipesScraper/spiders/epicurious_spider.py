"""
Scrape data from epicurious.com
"""
import scrapy
from scrapy.linkextractors import LinkExtractor
from extruct.w3cmicrodata import MicrodataExtractor
from extruct.jsonld import JsonLdExtractor

from RecipesScraper.items import RecipeItem


class Epicurious(scrapy.Spider):
  """Spider to scrape Epicurious (epicurious.com)"""
  name = "epicurious"
  edit_base = "http://www.epicurious.com/services/sitemap/recipes/editorial"
  editorial_recipes = ["{}/{}?page=1".format(edit_base, year)
                       for year in range(1998, 2018)]
  mem_base = "http://www.epicurious.com/services/sitemap/recipes/member"
  member_recipes = ["{}/{}?page=1".format(mem_base, year)
                    for year in range(2005, 2018)]
  start_urls = editorial_recipes + member_recipes

  def parse(self, response):
    """Parse the recipe list."""
    recipes = LinkExtractor(
        allow=("/recipes/.*/views")
    ).extract_links(response)
    if len(recipes) > 0:
      for recipe_link in recipes:
        yield scrapy.Request(recipe_link.url, callback=self.parse_item)

      base_url, page = response.url.split("=")
      yield scrapy.Request("{}={}".format(base_url, int(page) + 1),
                           callback=self.parse)
    else:
      print "Finished on {}".format(response.url)

  def parse_item(self, response):
    """Parse the recipe to get title and ingredients."""
    schema_type = "mde"
    mde = MicrodataExtractor()
    data = mde.extract(response.body)
    if len(data['items']) == 0:
      jslde = JsonLdExtractor()
      data = jslde.extract(response.body)
      schema_type = "jsonld"

    if schema_type == "mde":
      recipe = data['items'][2]['properties']
      recipe_output_item = RecipeItem()
      recipe_output_item['recipe_name'] = recipe['name']
      recipe_output_item['ingredients'] = [
          ingredient for ingredient in recipe['ingredients']
          if ingredient not in ['', 'Add all ingredients to list']
      ]
      recipe_tags = recipe['recipeCategory']
      if 'recipeCuisine' in recipe.keys():
        recipe_tags.append(recipe['recipeCuisine'])
      recipe_output_item['tags'] = recipe_tags
      try:
        recipe_output_item['description'] = recipe['description']
      except KeyError:
        recipe_output_item['description'] = None
      recipe_output_item['url'] = recipe['url']
    elif schema_type == "jsonld":
      recipe = data['items'][0]
      recipe_output_item = RecipeItem()
      recipe_output_item['recipe_name'] = recipe['name']
      recipe_output_item['ingredients'] = recipe['ingredients']
      recipe_output_item['tags'] = [tag['properties']['title']
                                    for tag in data['items'][1:]]
      try:
        recipe_output_item['description'] = recipe['description']
      except KeyError:
        recipe_output_item['description'] = None
      recipe_output_item['url'] = recipe['url']

    yield recipe_output_item
