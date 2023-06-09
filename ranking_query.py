from ast import literal_eval

import requests
import unidecode

from university import University
from supported_university import SupportedUniversity


def ask_arwu(name):
    # remove the unicode special chars
    name = unidecode.unidecode(name.replace(" ", "+"))
    # what you get is a dictionary in string, so just convert it
    ranking_dict = literal_eval(requests.get(f"https://www.shanghairanking.com/api/pub/v1/inst?name_en={name}&region"
                                             f"=&limit=&random=false").text)
    if not ranking_dict["data"]:
        return None
    return ranking_dict["data"][0]
