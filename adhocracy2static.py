import re, urllib.request
from urllib.parse import urljoin
import os


base_url = "https://normsetzung.cs.uni-duesseldorf.de"
base_domain = "normsetzung.cs.uni-duesseldorf.de"
targetDirectory = "page"

def main():
    if not os.path.exists(targetDirectory):
        os.mkdir(targetDirectory)

    crawledPages = 0
    failedPages = 0
    pages = [base_url]

    for page in pages:
        print("Crawling %s" % page)

        success, deltaNewURLs = crawl(page)

        if success:
            crawledPages += 1
        else:
            failedPages += 1

        for newURL in deltaNewURLs:
            if not newURL in pages and urlInDomainNamespace(newURL):
                if newURL[:4] == "http":
                    # includes http:, https:
                    # excludes mailto: and javascript:
                    pages.append(newURL)

    print("%i pages crawled (%i failed)" % (crawledPages, failedPages))


def crawl(url):
    try:
        content = urllib.request.urlopen(url).read().decode('utf-8')
        foundURLs = list(find_links(url, content))

        dateiname = stripProtocol(url)
        dateiname = dateiname.replace("/","")
        dateiname += ".txt"
        path = os.path.join(targetDirectory, dateiname)

        with open(path, "wb") as f:
            f.write(content.encode("utf-8"))

        return(True, foundURLs)
    except urllib.error.HTTPError as err:
        print("Page %s, Error %s" % (url, err))
        return(False, [])


def urlInDomainNamespace(url):
    url = stripProtocol(url)

    if "/" in url:
        domain = url[:url.index("/")]
    else:
        domain = url

    if domain == base_domain:
        return True
    else:
        print("Avoid URL %s" % url)
        return False


def stripProtocol(url):
    return url.replace("https://", "").replace("http://", "")


def find_links(base_url, s):
    for m in re.finditer(r"""(?is)<a[^>]*href[\s\n]*=[\s\n]*("[^"]*"|'[^']*')""", s):
        yield urljoin(base_url, m.group(1)[1:-1])

if __name__ == "__main__":
    main()
