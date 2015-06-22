import re, urllib.request
from urllib.parse import urljoin

 
base_url = "https://normsetzung.cs.uni-duesseldorf.de"

def main():
    s = urllib.request.urlopen(base_url).read().decode('utf-8')
    links = list(find_links(base_url, s))
    print(links)
    print (len(links))

    for link in links:
        
        with open("test.txt", "wb") as f:
         
            site=urllib.request.urlopen(link)
            site_content = site.read()
            f.write(site_content)
            
      
  
def find_links(base_url, s):
    for m in re.finditer(r"""(?is)<a[^>]*href[\s\n]*=[\s\n]*("[^"]*"|'[^']*')""", s):
        yield urljoin(base_url, m.group(1)[1:-1])

if __name__ == "__main__": 
    main()