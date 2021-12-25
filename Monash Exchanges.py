import unidecode
import csv
import requests
from bs4 import BeautifulSoup
from ast import literal_eval


class University:
    def __init__(self, name="", rank="10000", link="", location="", faculty=""):
        self.name = name
        self.rank = rank
        self.link = link
        self.location = location
        self.faculty = faculty

    def __repr__(self):
        return self.name + "\nranked " + self.rank + " in the world"


def main():
    monash_page = requests.get("https://www.monash.edu/study-abroad/overseas/exchange/exchange-partners").text
    soup = BeautifulSoup(monash_page, 'lxml')
    # get the raw html sections containing uni names and descriptions
    raw_info = soup.find_all("a", class_="box-featured__heading-link")
    # get the uni names and links from the page
    uni_list = get_uni_names_and_links(raw_info)
    # Start querying for ranking, using 2021 ARWU ranking here
    for university in uni_list:
        # debug use
        # print(university.name)
        info_dict = ask_ARWU(university.name)
        if info_dict:   # if the uni is found
            if info_dict["ranking"]:
                # for some reason, there are empty ranking (i.e. ranking="")
                university.rank = info_dict["ranking"]
            university.location = info_dict["region"]
    # sort it based on rankings, split to take care of 101-200th styled rankings
    uni_list.sort(key=lambda x: int(x.rank.split("-")[0]))
    # Writing to file cuz it takes too long to run each time
    with open("data.csv", "wt", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter=",")
        # headers
        writer.writerow(["Name", "Rank", "Link", "Location", "Faculty"])
        # write attributes
        for i in range(len(uni_list)):
            # print(list(uni_list[i].__dict__.values()))
            writer.writerow(list(uni_list[i].__dict__.values()))
        f.close()


def ask_ARWU(name):
    # remove the unicode special chars
    name = unidecode.unidecode(name.replace(" ", "+"))
    # what you get is a dictionary in string, so just convert it
    ranking_dict = literal_eval(requests.get(f"https://www.shanghairanking.com/api/pub/v1/inst?name_en={name}&region"
                                             f"=&limit=&random=false").text)
    if not ranking_dict["data"]:
        return None
    return ranking_dict["data"][0]


def get_uni_names_and_links(raw):
    res = []
    # get the text in the html
    uni_names = [i.text for i in raw]
    # get the links to monash introduction of the unis
    uni_links = [i["href"] for i in raw]
    # remove all the line breaks and redundant white spaces
    for i in range(len(uni_names)):
        uni_names[i] = uni_names[i].replace("\n", "")
        uni_names[i] = uni_names[i].replace("\r", "")
    # if there are [Uniname]-[Faculty] format, separate them and specify the faculty
        if "-" in uni_names[i]:
            res.append(University(name=uni_names[i].split("-")[0].strip(), faculty=uni_names[i].split("-")[-1].strip(),
                                  link=uni_links[i]))
        else:
            res.append(University(name=uni_names[i].strip(), link=uni_links[i]))
    return res


if __name__ == "__main__":
    main()
