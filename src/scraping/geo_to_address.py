
import os
import sys
path = os.path.dirname(__file__)
path = os.path.join(path, "..")
sys.path.insert(0, os.path.abspath(os.path.join(os.path.basename(path), "..")))
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import re
from pprint import pprint
import csv

import src.scraping.utilities as utilities

def find_postal(value):
    regex = r'(?=\()'  # finds open parenthesis
    closed_parenth = r'(?<=\))'  # finds close parentheis
    num_chunks = r'[0-9]+\W'  # Finds blocks of number codes.
    postal_code = r'[A-Za-z][0-9][A-Za-z]'
    num_check2 = r'(?=(?:.)(?<=[0-9][^A-Z](?:\s|[A-Za-z])))'

    n_check = r"neighbourhood"
    if re.findall(n_check, value, flags=re.IGNORECASE):
        neighbourhood = re.split(n_check, value, flags=re.IGNORECASE)[-1]
    else:
        neighbourhood = re.split(regex, value)
        if len(neighbourhood) > 1:
            neighbourhood = re.split(closed_parenth, neighbourhood[1])[0][1:-1]
           
    value = re.sub(regex, ",", value)
    

    postal = re.findall(postal_code, value)
    value = re.sub(num_chunks, ",", value)
    value = re.sub(num_check2, ",", value).split(",")
    value = [x.strip() for x in value if x != ""]
    value = [x if not x.startswith("(") else x[1:-1] for x in value]
    value = [x for x in value if not x == '-']
    # value = " ".join(value)
    
    return value, postal, neighbourhood

def find_address(*values, geo_points):

    with open("/Users/mathewzaharopoulos/dev/realestate_api/data/Postal codes Canada/CA.txt", "r") as f:
        docs = list(csv.reader(f, delimiter='\t'))

        docs_list = [y for x in docs for y in x]
        value, postal, neighbourhood = find_postal(values[0])
        if postal:
            value.append(postal[0])
        if neighbourhood:
            value.append(neighbourhood[0])
        intersection = set(docs_list) & set(value)

        points = []
    
        if geo_points:
            
            points.append('{:.3f}'.format(geo_points['lng']))
            points.append('{:.3f}'.format(geo_points['lat']))
            pattern = str("(" + "|".join(points) + ")")

        if intersection:
            matches = set()
            for idx, doc in enumerate(docs):

                if points:
                    m = re.findall(pattern, " ".join(doc))
                    if m:
                        matches.add(idx)

                try:
                    for v in intersection:
                        v = doc.index(v)
                        if v:
                            matches.add(idx)
                except:
                    continue
            
            matches = [docs[x] for x in matches]
            
            if geo_points:  # Checks for precision between postal and input 
                error = 1000
                min_error = 0
                for idx, interval in enumerate(matches):
                    lng = float(geo_points['lng']) - float(interval[10])
                    lat = float(geo_points['lat']) - float(interval[9])
                    if (lng + lat) < error:
                        error = lng + lat
                        min_error = idx

                matches[0] = matches[min_error]
                min_error = 1000

            keys = ['country_code', 'postal_code', 'place_name',
                    'admin_n1', 'admin_c1','admin_n2', 'admin_c2',
                    'admin_n3', 'admin_c3', 'lat', 'lng']
            mydict = {}
            for idx, k in enumerate(keys):
                    mydict[k] = matches[0][idx]

            # mydict = {key: value for key, value in mydict.items() if value}

            return mydict

