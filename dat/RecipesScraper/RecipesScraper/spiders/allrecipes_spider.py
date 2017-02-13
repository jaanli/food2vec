"""
Scrape data from allrecipes.com
"""
import scrapy
from scrapy.linkextractors import LinkExtractor
from extruct.w3cmicrodata import MicrodataExtractor
from extruct.jsonld import JsonLdExtractor

from RecipesScraper.items import RecipeItem


class AllRecipesSpider(scrapy.Spider):
  """Spider to scrape All Recipes (allrecipes.com)"""
  name = "allrecipes"

  start_urls = ["http://allrecipes.com/recipes/?page={}".format(page)
                for page in range(3000)]

  def parse(self, response):
    """Parse the recipe list."""
    recipes = LinkExtractor(allow=r"/recipe/\d+/.*").extract_links(response)
    if len(recipes) > 0:
      for recipe_link in recipes:
        yield scrapy.Request(recipe_link.url, callback=self.parse_item)

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
      recipe = data['items'][0]['properties']
      recipe_output_item = RecipeItem()
      recipe_output_item['recipe_name'] = recipe['name']
      recipe_output_item['ingredients'] = [
          ingredient for ingredient in recipe['ingredients']
          if ingredient not in ['', 'Add all ingredients to list']
      ]
      recipe_output_item['tags'] = [tag['properties']['title']
                                    for tag in data['items'][1:]]
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
