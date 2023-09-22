import requests


class Crawler:
    def __init__(self):
        self.headers = {
            # "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            # "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.8",
            # "Sec-Ch-Ua-Mobile": "?0",
            # "Sec-Ch-Ua-Platform": "Windows",
            # "Sec-Fetch-Dest": "document",
            # "Sec-Fetch-Mode": "navigate",
            # "Sec-Fetch-Site": "none",
            # "Sec-Fetch-User": "?1",
            # "Sec-Gpc": "1",
            # "Upgrade-Insecure-Requests":"1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
        }

    def get(self, url: str):
        return requests.get(url, headers=self.headers)


if __name__ == "__main__":
    test_url = ""
    crawler = Crawler()
    response = crawler.get(test_url)
    print(response.status_code, response.content.decode())
