"""
Download and parse sitemap for All Recipes.
"""
import urllib2
import StringIO
import gzip

from xml.etree import ElementTree


def get_sitemap(base_url, filename, out_file_path, compressed=True):
  """Get the sitemap XML.

  Parameters
  ----------
  base_url : str
    Base url of file location
  filename : str
    Filename on web
  out_file_path : str
    Desire file path to save to

  Returns
  -------
  None (file is downloaded)
  """
  response = urllib2.urlopen(base_url + filename)
  compressed_file = StringIO.StringIO()
  compressed_file.write(response.read())
  #
  # Set the file's current position to the beginning
  # of the file so that gzip.GzipFile can read
  # its contents from the top.
  #
  compressed_file.seek(0)

  if compressed:
    decompressed_file = gzip.GzipFile(fileobj=compressed_file, mode='rb')

    with open(out_file_path, 'w') as outfile:
      outfile.write(decompressed_file.read())
  else:
    with open(out_file_path, 'w') as outfile:
      outfile.write(compressed_file.read())


def get_seed_list(xml_file, base_url, url_part=""):
  """Get the list of urls for world cuisine.  Find the
  longest path available for a particular type of food.

  Parameters
  ----------
  xml_file : str
    The file path of the sitemap XML
  base_url : str
    The base url of the website being scraped
  url_part : str
    A part of the url to match in

  Returns
  -------
  list
    A list of urls
  """
  root = ElementTree.parse(xml_file).getroot()

  tree = {}
  for child in root:
    full_url = child[0].text
    if url_part in full_url:
      last_level = tree
      url_split = full_url.split("/")
      for level in url_split:
        if level not in ["", "http:", base_url] and not level.isdigit():
          if level in last_level:
            last_level = last_level[level]
          else:
            last_level[level] = {"url": full_url}

  return get_leaf_node_attribute(tree, "url")


def get_leaf_node_attribute(tree, attribute):
  """Recursively find an attribute of the leaf nodes of a tree.

  Parameters
  ----------
  tree : dict
    A dictionary of dictionaries tree structure
  attribute : str
    The attribute to find at the root nodes

  Returns
  -------
  list
    A list of attributes
  """
  leaf_nodes = []

  def get_leaf_node_attribute_helper(subtree, attribute):
    """Helper function to recursively find root node attributes.

    Parameters
    ----------
    subtree : dict
      A dictionary of dictionaries tree structure
    attribute: str
      The attribtue to find at the root nodes

    Returns
    -------
    None (either another function call is made or an item is appended
      to a list)
    """
    keys = subtree.keys()
    if keys == [attribute]:
      leaf_nodes.append(subtree[attribute])
    else:
      for key in keys:
        if key != attribute:
          get_leaf_node_attribute_helper(subtree[key], attribute)

  get_leaf_node_attribute_helper(tree, attribute)

  return leaf_nodes


def get_recursive_site_list(base_url):
  """Recursively get the list of recipes from epicurious.

  Parameters
  ----------
  base_url : str
    The url to start the recursive calls at

  Returns
  -------
  list
    A list of all of the recipe urls
  """
  root = ElementTree.fromstring(
      "\n".join(urllib2.urlopen(base_url).readlines())
  )

  url_list = []
  for child in root:
    full_url = child[0].text
    if "?" in full_url:
      url_list += get_recursive_site_list(full_url)
    else:
      url_list.append(full_url)

  return url_list


def get_and_parse_allrecipes_sitemap():
  """Get and parse the allrecipes sitemap."""
  # Sitemap:  http://allrecipes.com/gsindex.xml
  xml_file_path = "xml/allrecipes_sitemap.xml"
  get_sitemap("http://allrecipes.com/", "recipehubs.xml.gz", xml_file_path)
  seed_list = get_seed_list(xml_file_path, "allrecipes.com")
  with open("seed_lists/allrecipes_seed_list.txt", "wb") as outfile:
    outfile.write("\n".join(seed_list))


def get_and_parse_jamieoliver_sitemap():
  """Get and parse the Jamie Oliver sitemap."""
  xml_file_path = "xml/jamieoliver_sitemap.xml"
  get_sitemap("http://www.jamieoliver.com/recipes/", "sitemap.xml",
              xml_file_path, compressed=False)
  seed_list = get_seed_list(xml_file_path, "jamieoliver.com")
  with open("seed_lists/jamieoliver_seed_list.txt", "wb") as outfile:
    outfile.write("\n".join(seed_list))


def get_and_parse_myrecipes_sitemap():
  """Get and parse the myrecipes sitemap."""
  # It's split into two pages
  # Page one
  xml_file_path = "xml/myrecipes_sitemap_page1.xml"
  get_sitemap("http://www.myrecipes.com/", "recipe-sitemap.xml?page=1",
              xml_file_path, compressed=False)
  seed_list = get_seed_list(xml_file_path, "myrecipes.com")
  with open("seed_lists/myrecipes_seed_list.txt", "wb") as outfile:
    outfile.write("\n".join(seed_list))

  # Page two
  xml_file_path = "xml/myrecipes_sitemap_page2.xml"
  get_sitemap("http://www.myrecipes.com/", "recipe-sitemap.xml?page=2",
              xml_file_path, compressed=False)
  seed_list = get_seed_list(xml_file_path, "myrecipes.com")
  with open("seed_lists/myrecipes_seed_list.txt", "ab") as outfile:
    outfile.write("\n".join(seed_list))


def get_and_parse_epicurious_sitemap():
  """Get and parse the epicurious sitemap."""
  member_recipes = get_recursive_site_list(
      "http://www.epicurious.com/sitemap.xml/member-recipes"
  )
  editorial_recipes = get_recursive_site_list(
      "http://www.epicurious.com/sitemap.xml/editorial-recipes"
  )

  seed_list = member_recipes + editorial_recipes
  with open("seed_lists/epicurious_seed_list.txt", "ab") as outfile:
    outfile.write("\n".join(seed_list))


if __name__ == "__main__":
  get_and_parse_allrecipes_sitemap()
  get_and_parse_jamieoliver_sitemap()
  get_and_parse_myrecipes_sitemap()
  get_and_parse_epicurious_sitemap()
