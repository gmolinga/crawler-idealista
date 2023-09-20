import json
import re

from bs4 import BeautifulSoup

from crawler import Crawler

DETAILS_ENDPOINT = "https://www.idealista.com/inmueble/"
REGEX_UTAG_DATA = re.compile("var utag_data = (.*?);")

class Details:
    def __init__(self):
        self.crawler = Crawler()

    def _build_url_from_id(self, id:int):
        return DETAILS_ENDPOINT + str(id)

    def get_details(self, id:int):
        url = self._build_url_from_id(id)
        page = self.crawler.get(url)
        soup = BeautifulSoup(page.content.decode())
        utag_data = json.loads(
            [
                catch
                for catch in 
                [
                    REGEX_UTAG_DATA.search(script.string)
                    for script in soup.find_all("script")
                    if isinstance(script.string,str)
                ]
                if catch
            ][0][1]
        )
        details = {
            **utag_data["ad"]
        }
        return details
    

if __name__ == "__main__":
    id = ""
    details = Details()
    response = details.get_details(id)
    print(response)
    with open(f"{id}.json", "w", encoding="utf8") as f:
        f.write(json.dumps(response))