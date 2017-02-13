"""
Item processor utilities
"""


def remove_extra_whitespace(item):
  """Remove extra whitespace from a string.

  Parameters
  ----------
  item : str
    A string

  Returns
  -------
  The same string with extra whitespace removed
  """
  return " ".join(item.strip().split())
