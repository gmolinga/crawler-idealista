import json
import re
from typing import Optional, List

from bs4 import BeautifulSoup

from crawler import Crawler
from details import Details
from models.property import MainCategory


REGEX_UTAG_DATA = re.compile("var utag_data = (.*?);")


class Discover:
    def __init__(self, details: Optional[Details] = None):
        self.crawler = Crawler()
        if isinstance(details, Details):
            self.details = Details
            self._extract_details = True
        else:
            self._extract_details = False

    def _build_url(
        self,
        main_category_to_search: MainCategory,
        area: List[str],
        current_page_number: int = 1,
    ):
        main_endpoint = "https://www.idealista.com/"
        action = f"venta-{main_category_to_search.value}/"

        if len(area) == 1:
            zone = f"{area[0]}-provincia/"
        elif len(area) == 2:
            zone = f"{area[0]}-{area[1]}/"
        elif len(area) == 3:
            zone = f"{area[0]}-{area[1]}/"
        else:
            zone = f"{area[1]}/{area[2]}/"

        if current_page_number > 1:
            page = f"pagina-{current_page_number}.htm"
        else:
            page = ""

        url = main_endpoint + action + zone + page
        return url

    def search(
        self,
        main_category_to_search: MainCategory,
        area: List[str],
        yield_current_page_number: bool = False,
    ):
        url = self._build_url(main_category_to_search, area)
        page = self.crawler.get(url)
        soup = BeautifulSoup(page.content.decode())
        utag_data = json.loads(
            [
                catch
                for catch in [
                    REGEX_UTAG_DATA.search(script.string)
                    for script in soup.find_all("script")
                    if isinstance(script.string, str)
                ]
                if catch
            ][0][1]
        )
        current_page_number = int(utag_data["list"]["currentPageNumber"])
        details = utag_data["list"]["ads"]
        total_pages = int(utag_data["list"]["totalPageNumber"])
        if yield_current_page_number:
            yield current_page_number, details
        else:
            yield details
        for i in range(2, total_pages + 1):
            url = self._build_url(main_category_to_search, area, current_page_number=i)
            page = self.crawler.get(url)
            soup = BeautifulSoup(page.content.decode())
            utag_data = json.loads(
                [
                    catch
                    for catch in [
                        REGEX_UTAG_DATA.search(script.string)
                        for script in soup.find_all("script")
                        if isinstance(script.string, str)
                    ]
                    if catch
                ][0][1]
            )
            current_page_number = int(utag_data["list"]["currentPageNumber"])
            details = utag_data["list"]["ads"]
            if yield_current_page_number:
                yield current_page_number, details
            else:
                yield details


if __name__ == "__main__":
    main_category = MainCategory.HOME
    area = ["barcelona", "barcelona"]
    discover = Discover()
    responses = discover.search(main_category, area)
    for n_page, response in enumerate(responses):
        print(response)

        filename = f"{main_category.name}-{'_'.join(area)}-{n_page}"
        if (
            isinstance(response, str)
            or isinstance(response, list)
            or isinstance(response, dict)
        ):
            with open(f"{filename}.json", "w", encoding="utf8") as f:
                f.write(json.dumps(response))
        else:
            with open(f"{filename}.html", "w", encoding="utf8") as f:
                f.write(response.content.decode())
