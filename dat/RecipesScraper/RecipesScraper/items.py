# -*- coding: utf-8 -*-
import scrapy


class RecipeItem(scrapy.Item):
    """Info from recipe to be collected."""
    recipe = scrapy.Field()
    ingredients = scrapy.Field()
    tags = scrapy.Field()
