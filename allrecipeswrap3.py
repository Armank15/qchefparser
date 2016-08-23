from bs4 import BeautifulSoup
import csv
import sys
import urllib
import time 

# These are some example websites
allrecipesexample = "http://allrecipes.com/recipes/?grouping=all"
#"http://allrecipes.com/search/results/?wt=chicken&sort=re"



def GetCategories(html) :
	allrecipes = []
	soup = BeautifulSoup(html, "html.parser")

	categoryurl = soup.find_all("a", class_="hero-link__item")
	for r in categoryurl:
		url = r.get('href')
		if url[:8] == "/recipes" :
			if not url in allrecipes :
				allrecipes.append(url)

	time.sleep(0.5)
	print "\n".join(allrecipes)
	return allrecipes


sock = urllib.urlopen(allrecipesexample)  
html = sock.read()
sock.close()
GetCategories	(html)