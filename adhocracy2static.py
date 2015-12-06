import re, urllib.request
from urllib.parse import urljoin
import os


base_url = "https://normsetzung.cs.uni-duesseldorf.de"
targetDirectory = "page"

def main():
    if not os.path.exists(targetDirectory):
        os.mkdir(targetDirectory)

    x=0
    s = urllib.request.urlopen(base_url).read().decode('utf-8')
    links = list(find_links(base_url, s))
    links.remove('mailto:normsetzung-support@cs.uni-duesseldorf.de')
    links.remove(links[9])
    links.remove(links[0])
    links.remove(links[0])
    print(links)
    print (len(links))

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
                    x+=1
            except urllib.error.HTTPError as err:
                print("Code %s Error %s" % (link, err))

def find_links(base_url, s):
    for m in re.finditer(r"""(?is)<a[^>]*href[\s\n]*=[\s\n]*("[^"]*"|'[^']*')""", s):
        yield urljoin(base_url, m.group(1)[1:-1])

if __name__ == "__main__":
    main()
