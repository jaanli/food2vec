"""
Scrape data from allrecipes.com
"""
import re
import scrapy
from RecipesScraper.items import RecipeItem


class AllRecipesSpider(scrapy.Spider):
    """Spider to scrape All Recipes (allrecipes.com)"""
    name = "allrecipes"

    with open("sitemap/allrecipes_seed_list.txt") as seedfile:
        start_urls = ["{}?page=1".format(url.strip()) for url in seedfile.readlines()]

    def parse(self, response):
        """Parse recipe page."""
        recipes = response.css('article.grid-col--fixed-tiles')
        if len(recipes) > 0:
            for recipe in recipes:
                try:
                    recipe_href = response.urljoin(recipe.css('a::attr(href)').extract_first())
                    if 'video' not in recipe_href and recipe_href != response.url:
                        yield scrapy.Request(recipe_href, callback=self.parse_recipe)
                except AttributeError:
                    self.log("Skipped empty article")

            base_url, page_info = response.url.split("?")
            page_number = int(page_info.split("=")[1])
            next_page = "{}?page={}".format(base_url, page_number + 1)
            yield scrapy.Request(next_page, callback=self.parse)

    def parse_recipe(self, response):
        """Parse the recipe to get title and ingredients."""
        recipe_name = self.remove_non_ascii(response.css("h1.recipe-summary__h1::text").extract_first())
        ingredients = response.css("span.recipe-ingred_txt::text").extract()
        recipe_tags = [li.css("span::text").extract_first().strip() for li in response.css("ul.breadcrumbs li")]
        #recipe_tags = all_tags[(all_tags.index("World Cuisine") + 1):]
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
