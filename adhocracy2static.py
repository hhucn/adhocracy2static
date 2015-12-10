import re, urllib.request
from urllib.parse import urljoin
import os


base_url = "https://normsetzung.cs.uni-duesseldorf.de"
targetDirectory = "page"

def main():
    if not os.path.exists(targetDirectory):
        os.mkdir(targetDirectory)

    crawledPages = 0
    failedPages = 0

    deltaCrawledPages, deltaFailedPages = crawl(base_url)
    crawledPages += deltaCrawledPages
    failedPages += deltaFailedPages

    print("%i pages crawled (%i failed)" % (crawledPages, failedPages))


def crawl(url):
    crawledPages = 0
    failedPages = 0

    s = urllib.request.urlopen(base_url).read().decode('utf-8')
    links = list(find_links(base_url, s))
    print(links)

    for link in links:
        if not link[:7] == "mailto:":
            dateiname = link.replace("/","")
            dateiname = dateiname.replace("https://", "")
            dateiname = dateiname.replace("http://", "")

            path = os.path.join(targetDirectory, dateiname + ".txt")

            try:
                site = urllib.request.urlopen(link)
                with open(path, "wb") as f:
                    site_content = site.read()
                    f.write(site_content)
                    crawledPages += 1
            except urllib.error.HTTPError as err:
                print("Page %s, Error %s" % (link, err))
                failedPages += 1

    return (crawledPages, failedPages)


def find_links(base_url, s):
    for m in re.finditer(r"""(?is)<a[^>]*href[\s\n]*=[\s\n]*("[^"]*"|'[^']*')""", s):
        yield urljoin(base_url, m.group(1)[1:-1])

if __name__ == "__main__":
    main()
