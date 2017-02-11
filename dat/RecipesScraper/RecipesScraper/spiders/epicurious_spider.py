"""
Scrape data from epicurious.com
"""
import re
import scrapy
from RecipesScraper.items import RecipeItem


class EpicuriousScraper(scrapy.Spider):
    """Spider to scrape Epicurious (epicurious.com)"""
    name = "epicurious"

    with open("sitemap/seed_lists/epicurious_seed_list.txt") as seedfile:
        start_urls = [url.strip() for url in seedfile.readlines()]

    def parse(self, response):
        """Parse the recipe to get title and ingredients."""
        recipe_name = self.remove_non_ascii(response.css('h1[itemprop="name"]::text').extract_first().strip())
        ingredients = [" ".join(tag.split()) for tag in response.css("li.ingredient::text").extract()]
        recipe_tags = [tag for tag in response.css("dl.tags").css("dt::text").extract()]
        self.log("Scraped {}".format(recipe_name))

        recipe = RecipeItem()
        recipe['recipe'] = recipe_name
        recipe['ingredients'] = ingredients
        recipe['tags'] = recipe_tags
        recipe['url'] = response.url

        yield recipe

    @staticmethod
    def remove_non_ascii(text):
        """Remove the non ascii characters."""
        if text is None:
            return None
        else:
            return ''.join([i if ord(i) < 128 else ' ' for i in text])
