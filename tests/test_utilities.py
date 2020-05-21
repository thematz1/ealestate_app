"""Support methods for testing units"""
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def data_load(folder_type):
    """Returns test data by property type."""

    # Path to data folders
    folders = {
      "commercial": ["../data/Centris Website/commercial"],
      "single-home": ["../data/Centris Website/single_home"],
      "business": ["../data/Centris Website/business"],
      "lot": ["../data/Centris Website/lot/"],
      "condo": ["../data/Centris Website/condo"],
      "plex": ["../data/Centris Website/plex"],
      "income": ["../data/Centris Website/income/"]
    }

    if folder_type not in folders:
      raise TypeError('Invalid folder type')

    data_paths = folders[folder_type]
    
    # Return list of html files
    for data_path in data_paths:
      for file in os.listdir(data_path):
          if file.endswith(".html"):
              yield os.path.join(data_path, file)


def load_page(path):
    """Returns the HTML file opened."""
    with open(path, 'r') as f:
        yield f
