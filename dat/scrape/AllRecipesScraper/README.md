# All Recipes Scraper

This scraper takes in the sitemap list of recipe hubs and scrapes all of the recipes from each one.

Start the scraper:

```bash
nohup scrapy crawl allrecipes %
```

This will create a JSON file `recipes.json` in the current directory.
