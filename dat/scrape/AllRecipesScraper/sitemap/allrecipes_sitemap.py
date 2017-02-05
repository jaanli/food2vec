"""
Download and parse sitemap for All Recipes.
"""
import urllib2
import StringIO
import gzip

from xml.etree import ElementTree


def get_sitemap(base_url, filename, out_file_path):
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

    decompressed_file = gzip.GzipFile(fileobj=compressed_file, mode='rb')

    with open(out_file_path, 'w') as outfile:
        outfile.write(decompressed_file.read())


def get_seed_list(xml_file, url_part=""):
    """Get the list of urls for world cuisine.  Find the
    longest path available for a particular type of food.

    Parameters
    ----------
    xml_file : str
        The file path of the sitemap XML

    url_part : str


    Returns
    -------
    list
        A list of urls
    """
    tree = ElementTree.parse(xml_file)
    root = tree.getroot()

    world_cuisine_tree = {}
    for child in root:
        full_url = child[0].text
        if url_part in full_url:
            last_level = world_cuisine_tree
            for level in full_url.split("/")[5:-1]:
                if level in last_level:
                    last_level = last_level[level]
                else:
                    last_level[level] = {"url": full_url}

    return get_leaf_node_attribute(world_cuisine_tree, "url")


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


def main():
    """Main function."""
    # Sitemap:  http://allrecipes.com/gsindex.xml
    xml_file_path = "recipehubs.xml"
    get_sitemap("http://allrecipes.com/", "recipehubs.xml.gz", xml_file_path)
    seed_list = get_seed_list(xml_file_path)
    with open("allrecipes_seed_list.txt", "wb") as outfile:
        outfile.write("\n".join(seed_list))


if __name__ == "__main__":
    main()
