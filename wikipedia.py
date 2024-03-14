import requests as rq
from bs4 import BeautifulSoup as bs
import re
import random as rand


# Creates a random seed based on the system's date and time
# Different from the book. By default seed() uses the date and time
rand.seed()


## Attempts to get the HTML from the url parameter. If unsuccessful, will print an error message and return None.
## If successful, will return the HTML from the URL
def getHTML(url):
    try:
        r = rq.get(url, allow_redirects=True)
    except rq.ConnectionError:
        print("Unable to connect to: " + url)
        return None
    except rq.HTTPError:
        print("HTTPError: " + url)
        return None
    except rq.Timeout:
        print("Timeout while trying to connect to: " + url)
        return None

    return bs(r.content, "html.parser")


def getLinks(articleUrl):
    # Every link which redirects to another Wikipedia page follows these 3 rules:
    #   1. They are contained within a div with id "bodyContent"
    #   2. They begin with /wiki/
    #   3. They do not contain a :
    # This line finds the div (1), and then finds all the links within it which match (2) and (3)
    soup = getHTML("http://en.wikipedia.org{}".format(articleUrl))
    return soup.find("div", {"id": "bodyContent"}).find_all(
        "a", href=re.compile("^(/wiki/)((?!:).)*$")
    )


pages = set()


def getMoreLinks(articleUrl):
    soup = getHTML("http://en.wikipedia.org{}".format(articleUrl))
    try:
        print(soup.h1.get_text())
        print(soup.find(id="mw-content-text").find("p")[0])
        print(soup.find(id="ca-edit").find("span")).find("a").attrs["href"]
    except AttributeError:
        print("Page is missing something. Continuing...")
    for link in soup.find_all("a", href=re.compile("^(/wiki/)")):
        if "href" in link.attrs:
            if link.attrs["href"] not in pages:
                newPage = link.attrs["href"]
                print("-" * 20)
                print(newPage)
                pages.add(newPage)
                getMoreLinks(newPage)


def kevinBacon():
    links = getLinks("/wiki/Kevin_Bacon")
    its = 0
    while len(links) > 0 and its < 100:
        newArticle = links[rand.randint(0, len(links) - 1)].attrs["href"]
        print(newArticle)
        links = getLinks(newArticle)
        its += 1


### Definitions above
kevinBacon()
