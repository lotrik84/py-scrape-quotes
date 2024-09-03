from dataclasses import dataclass
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup, Tag

BASE_URL = "https://quotes.toscrape.com/"


@dataclass
class Quote:
    text: str
    author: str
    tags: list[str]


def parse_single_quote(quote_soup: Tag) -> Quote:
    return Quote(
        text=quote_soup.select_one(".text").text,
        author=quote_soup.select_one(".author").text,
        tags=[tag.text for tag in quote_soup.select(".tags > .tag")],
    )


def parse_page_with_quotes(quotes_soup: BeautifulSoup) -> list[Quote]:
    return [
        parse_single_quote(quote) for quote in quotes_soup.select(".quote")
    ]


def main(output_csv_path: str) -> None:
    page = requests.get(BASE_URL).content
    first_page_soup = BeautifulSoup(page, "html.parser")

    all_quotes = parse_page_with_quotes(first_page_soup)

    page_number = 2
    while True:
        print(f"Page #{page_number}")
        page = requests.get(urljoin(BASE_URL, f"/page/{page_number}")).content
        soup = BeautifulSoup(page, "html.parser")

        if not soup.text.__contains__("No quotes found!"):
            all_quotes.extend(parse_page_with_quotes(soup))
            page_number += 1
        else:
            break

    print(all_quotes)


if __name__ == "__main__":
    main("quotes.csv")
