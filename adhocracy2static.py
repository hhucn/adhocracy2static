import re, urllib.request
from urllib.parse import urljoin
import os
import hashlib


base_url = "https://normsetzung.cs.uni-duesseldorf.de"
base_domain = "normsetzung.cs.uni-duesseldorf.de"
targetDirectory = "page"


class suppressRedirectHandler(urllib.request.HTTPRedirectHandler):
    # see comments in main()
    # code taken from urllib.request.HTTPRedirectHandler.redirect_request

    def redirect_request(self, req, fp, code, msg, headers, newURL):
        oldHeaders = ("content-length", "content-type")
        newHeaders = dict((k, v) for k, v in req.headers.items()
                          if k.lower() not in oldHeaders)

        quotedURL = urllib.parse.quote(newURL, "!*'();:@&=+$,/?%#[]-_.~")
        print("Redirect to %s" % quotedURL)

        if urlInDomainNamespace(quotedURL):
            return urllib.request.Request(quotedURL,
                           headers=newHeaders,
                           origin_req_host=req.origin_req_host,
                           unverifiable=True)
        else:
            return None


def main():
    # Inject a custom handler into the urllib handler queue.
    # There is no quick way to interrupt urllib from following redirects.
    # This is a problem here because urllib needs ASCII URLs, but the target
    # URL (the one redirected to) may contain UTF-8 chars.
    opener = urllib.request.build_opener(suppressRedirectHandler)
    urllib.request.install_opener(opener)

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
                    pages.append(urllib.parse.quote(newURL, "!*'();:@&=+$,/?%#[]-_.~"))

    print("%i pages crawled (%i failed)" % (crawledPages, failedPages))


def crawl(url):
    try:
        connection = urllib.request.urlopen(url)
        if "text/html" in connection.getheader("Content-Type"):
            content = connection.read().decode('utf-8')
            foundURLs = list(find_links(url, content))
        else:
            content = connection.read()
            foundURLs = []

        dateiname = stripProtocol(url)
        dateiname = dateiname.replace("/","")
        dateiname += ".txt"

        if len(dateiname) > 255:
            shaname = hashlib.sha256(bytes(dateiname, "utf-8")).hexdigest()
            print("Pathlength > 255: %s, using %s" % (dateiname, shaname))
            dateiname = shaname

        path = os.path.join(targetDirectory, dateiname)

        with open(path, "wb") as f:
            if type(content) is str:
                content = content.encode("utf-8")
            f.write(content)

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
