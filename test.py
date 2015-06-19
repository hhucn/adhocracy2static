import re, urllib.request
from urllib.parse import urljoin

 
b = "https://normsetzung.cs.uni-duesseldorf.de"
s = urllib.request.urlopen(b).read().decode('utf-8')
 
def get_a(b, s):
    for m in re.finditer(r"""(?is)<a[^>]*href[\s\n]*=[\s\n]*("[^"]*"|'[^']*')""", s):
        yield urljoin(b, m.group(1)[1:-1])
 
s= list(get_a(b, s))
#print(s)
x=0
file = open("test.txt", "w")

while x < len(s):   
        site=urllib.request.urlopen(s[x])
        a=site.read()
        file.write(str(a))
        x+=1
file.close()
 