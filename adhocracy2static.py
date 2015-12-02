import re, urllib.request
from urllib.parse import urljoin


base_url = "https://normsetzung.cs.uni-duesseldorf.de"

def main():
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
            dateiname = link.replace("/","")
            dateiname = dateiname.replace("https", "")
            dateiname = dateiname.replace("http", "")

            with open(dateiname+".txt", "wb") as f:
                site=urllib.request.urlopen(link)
                site_content = site.read()
                f.write(site_content)
                x+=1

def find_links(base_url, s):
    for m in re.finditer(r"""(?is)<a[^>]*href[\s\n]*=[\s\n]*("[^"]*"|'[^']*')""", s):
        yield urljoin(base_url, m.group(1)[1:-1])

if __name__ == "__main__":
    main()
