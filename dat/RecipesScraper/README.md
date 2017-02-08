# Spiders

This folder contains various spider to scrape different recipe websites.  

## Spiders

* [All Recipes](http://allrecipes.com/)
* [Jamie Oliver](http://www.jamieoliver.com/)

## Running a spider

Each spider takes in a corresponding seed list (available in [`sitemap/seed_lists`](sitemap/seed_lists)) and either scrapes the recipe itself or follow recipes links on the section page.

To run a spider, use the following command:

```bash
nohup scrapy crawl <spider_name> &
```

where `<spider name>` is the name of the spider (`allrecipes` or `jamieoliver` for now).  This will create a JSON file named `<spider_name>_recipes.json` in the [`output`](output) folder.

Since this will be a long running process, it's a good idea to run it as a background process in no-hangup mode.

```bash
nohup scrapy crawl <spider_name> &
```
