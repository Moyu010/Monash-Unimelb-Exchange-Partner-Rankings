from supported_university import SupportedUniversity
from university import University


class Monash(SupportedUniversity):
    URL = "https://www.monash.edu/study-abroad/overseas/exchange/exchange-partners"

    def __init__(self):
        super().__init__(Monash.URL)

    def get_exchange_info(self):
        # get the raw html sections containing uni names and descriptions
        raw = self._soup.find_all("a", class_="box-featured__heading-link")
        # get the uni names and links from the page
        res = []
        # get the text in the html
        uni_names = [i.text for i in raw]
        # get the links to monash introduction of the unis
        uni_links = [i["href"] for i in raw]
        # remove all the line breaks and redundant white spaces
        for i in range(len(uni_names)):
            uni_names[i] = uni_names[i].replace("\n", "")
            uni_names[i] = uni_names[i].replace("\r", "")
            # if there are [Uni name]-[Faculty] format, separate them and specify the faculty
            if "-" in uni_names[i]:
                res.append(
                    University(name=uni_names[i].split("-")[0].strip(), faculty=uni_names[i].split("-")[-1].strip(),
                               link=uni_links[i]))
            else:
                res.append(University(name=uni_names[i].strip(), link=uni_links[i]))
        return res
