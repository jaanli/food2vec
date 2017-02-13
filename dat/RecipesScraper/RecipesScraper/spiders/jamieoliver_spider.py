"""
Scrape data from jamieoliver.com
"""
import scrapy
from RecipesScraper.items import RecipeItem


class JamieOliverScraper(scrapy.Spider):
  """Spider to scrape Jamie Oliver (jamieoliver.com)"""
  name = "jamieoliver"

  with open("sitemap/seed_lists/jamieoliver_seed_list.txt") as seedfile:
    start_urls = [url.strip() for url in seedfile.readlines()]

  def parse(self, response):
    """Parse recipe page."""
    recipes = response.css('div.recipe-block')
    if len(recipes) > 0:
      for recipe in recipes:
        try:
          recipe_href = response.urljoin(
              recipe.css('a::attr(href)').extract_first()
          )
          yield scrapy.Request(recipe_href, callback=self.parse_recipe)
        except AttributeError:
          self.log("Skipped empty article")
    else:
      self.parse_recipe(response)

  def parse_recipe(self, response):
    """Parse the recipe to get title and ingredients."""
    recipe_name = self.remove_non_ascii(
        response.css("h1.hidden-xs::text").extract_first()
    )
    ingredients_list = response.css("ul.ingred-list")
    ingredients = [' '.join(ingred.strip().split()).replace(' , ', ', ')
                   for ingred in ingredients_list.css("li::text").extract()]
    url_tags = [u" ".join(tag.split("-")).capitalize()
                for tag in response.url.split("/")[4:-2]]
    html_tags = response.css("div.tags-list").css("a::text").extract()
    recipe_tags = url_tags + html_tags
    self.log("Scraped {}".format(recipe_name))

    recipe = RecipeItem()
    recipe['recipe'] = recipe_name
    recipe['ingredients'] = ingredients
    recipe['tags'] = recipe_tags

    yield recipe

  @staticmethod
  def remove_non_ascii(text):
    """Remove the non ascii characters."""
    if text is None:
      return None
    else:
      return ''.join([i if ord(i) < 128 else ' ' for i in text])
