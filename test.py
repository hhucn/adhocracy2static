import urllib.request

#lädt den Quellcode und speichert in in einer Datei
website = "https://normsetzung.cs.uni-duesseldorf.de"
t = urllib.request.urlopen(website)
f = open ("website.txt", "w")
f.write(str(t.read()))
