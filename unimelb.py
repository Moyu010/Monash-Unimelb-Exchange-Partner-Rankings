from supported_university import SupportedUniversity
from university import University


class Unimelb(SupportedUniversity):
    URL = "https://studyos.students.unimelb.edu.au/index.cfm?FuseAction=Programs.SearchResults\
           &Program_Name=&Program_Type_ID=1&pi=%7F&pc=%7F&pr=%7F&pt=%7F&Partner_ID=ANY&p_10001\
           =Exchange%7F&p_10001_t=MULTI&p_10003=%7F&p_10003_t=MULTI&p_10004=%7F&p_10004_t=MULTI\
           &p_10002=%7F&p_10002_t=MULTI&p_10000=%7F&p_10000_t=MULTI&Sort=Program_Name&Order=asc\
           &pp=10001%2C10003%2C10004%2C10002%2C10000"

    def __init__(self):
        super().__init__(Unimelb.URL)

    def get_exchange_info(self):
        raw = self._soup.find_all("td", class_=None)
        res = []
        # get the text in the html
        for i in raw:
            try:
                name = i.find("a")["title"]
                link = "https://studyos.students.unimelb.edu.au/" + i.find("a")["href"]
                if "-" in name:
                    res.append(University(name=name.split("-")[0].strip(), faculty=name.split("-")[-1].strip(),
                                          link=link))
                else:
                    res.append(University(name=name.strip(), link=link))
            except TypeError:
                pass
        return res
