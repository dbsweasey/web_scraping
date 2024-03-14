import requests as req
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import re
import random

pages = set()
random.seed()


## Must include error/exception checking to ensure connections and attributes are correct


def getInternalLinks(bs, includeUrl):
    includeUrl = "{}://{}".format(
        urlparse(includeUrl).scheme, urlparse(includeUrl).netloc
    )
    internalLinks = []
    links = bs.find_all("a", href=re.compile("^(\/|.*" + includeUrl + ")"))
    for link in links:
        if link.attrs["href"] is not None:
            if link.attrs["href"] not in internalLinks:
                if link.attrs["href"].startswith("/"):
                    internalLinks.append(includeUrl + link.attrs["href"])
                else:
                    internalLinks.append(link.attrs["href"])
    return internalLinks


def getExternalLinks(bs, excludeUrl):
    externalLinks = []
    for link in bs.find_all(
        "a", href=re.compile("^(www|http)((?!" + excludeUrl + ").)*$")
    ):
        if link.attrs["href"] is not None:
            if link.attrs["href"] not in externalLinks:
                externalLinks.append(link.attrs["href"])
    return externalLinks


def getRandomExternalLink(startingPage):
    html = req.get(startingPage)
    bs = BeautifulSoup(html.content, "html.parser")
    externalLinks = getExternalLinks(bs, urlparse(startingPage).netloc)
    if len(externalLinks) == 0:
        print("No external links, looking around site for one.")
        domain = "{}://{}".format(
            urlparse(startingPage).scheme, urlparse(startingPage).netloc
        )
        internalLinks = getInternalLinks(bs, domain)
        if not internalLinks:
            print("No internal links, reached a dead end.")
            exit()
        return getRandomExternalLink(
            internalLinks[random.randint(0, len(internalLinks) - 1)]
        )
    else:
        return externalLinks[random.randint(0, len(externalLinks) - 1)]


def followExternalOnly(startingSite):
    externalLink = getRandomExternalLink(startingSite)
    print("Random external link is: {}".format(externalLink))
    followExternalOnly(externalLink)


### Put any link here
followExternalOnly("http://oreilly.com")
