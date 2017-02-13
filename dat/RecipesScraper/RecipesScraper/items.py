"""
Recipe item pulled from each recipe.
"""
import scrapy
from scrapy import Item
from scrapy.loader.processors import MapCompose

from RecipesScraper.utils import remove_extra_whitespace


class RecipeItem(Item):
  """Info from recipe to be collected."""
  recipe_name = scrapy.Field(
      input_processor=MapCompose(remove_extra_whitespace)
  )
  ingredients = scrapy.Field(
      input_process=MapCompose(remove_extra_whitespace)
  )
  tags = scrapy.Field(
      input_process=MapCompose(remove_extra_whitespace)
  )
  url = scrapy.Field(
      input_process=MapCompose(remove_extra_whitespace)
  )
  description = scrapy.Field(
      input_process=MapCompose(remove_extra_whitespace)
  )
