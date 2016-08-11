from bs4 import BeautifulSoup
import csv
import sys
import urllib
import time 

# These are some example websites
allrecipesexample = "http://allrecipes.com/search/results/?wt=chicken&sort=re"
#"http://allrecipes.com/search/results/?wt=chicken&sort=re"



allrecipes = []


def getIngredientsAllRecipes(soup) :
	results = [ ]

	list_1 = soup.find("ul", id="lst_ingredients_1")
	list_2 = soup.find("ul", id="lst_ingredients_2")

	spans = list_1.find_all("span", class_="recipe-ingred_txt added") 
	spans2 = list_2.find_all("span", class_="recipe-ingred_txt added")

	combinedspan = spans + spans2
	for ing in combinedspan:
		results.append(ing.contents)
	return results

def getNameAllRecipes(soup) :
	results = [ ]
	name = soup.find("h1", itemprop="name")
	return name.contents


def getCookTimeAllRecipes(soup) :

	soup = BeautifulSoup(html, "html.parser")
	CookTime = soup.find("span", class_="ready-in-time")
	return CookTime.contents

def getRatingAllRecipes(soup) : 

	ratingStars = soup.find("div", class_="rating-stars")

	return float(ratingStars['data-ratingstars']) 


def getStepsAllRecipes(soup) : 

	results = [ ]
	soup = BeautifulSoup(html, "html.parser")
	#StepsList = soup.find_all("li", class_="step")
	StepsList = soup.find_all("span", class_="recipe-directions__list--item")
	for steps in StepsList :
		results.append(steps.contents)
	return results

def getServingSizeAllRecipes(soup) : 
	
	ServingSize = soup.find("input", id="servings")
	return int(ServingSize['data-original'])

 
def getIngredients(soup) :
	
	meta = soup.find("meta", property="og:url")
	if meta: 

		print meta['content']
		if meta['content'].startswith("http://allrecipes.com") :
			return getIngredientsAllRecipes(soup)
		elif meta['content'].startswith("http://www.foodnetwork.com") : 
			return getIngredientsFoodNetwork(htm)
	print "UNKNOWN WEBSITE, PLEASE ADD!"
	return []

def getName(soup) :
	

	meta = soup.find("meta", property="og:url")
	if meta: 
		if meta['content'].startswith("http://allrecipes.com") :
			return getNameAllRecipes(soup)
		elif meta['content'].startswith("http://www.foodnetwork.com") : 
			return getIngredientsFoodNetwork(htm)
	print "UNKNOWN WEBSITE, PLEASE ADD!"
	return []

def getRating(soup) : 
	
	meta = soup.find("meta", property="og:url")
	if meta: 
		if meta['content'].startswith("http://allrecipes.com") :
			return getRatingAllRecipes(soup)
		elif meta['content'].startswith("http://www.foodnetwork.com") : 
			return getIngredientsFoodNetwork(htm)
	print "UNKNOWN WEBSITE, PLEASE ADD!"
	return []

def getCookTime(soup) :
	

	meta = soup.find("meta", property="og:url")
	if meta: 
		if meta['content'].startswith("http://allrecipes.com") :
			return getCookTimeAllRecipes(soup)
		elif meta['content'].startswith("http://www.foodnetwork.com") : 
			return getIngredientsFoodNetwork(htm)
	print "UNKNOWN WEBSITE, PLEASE ADD!"
	return []

def getServingSize(soup) : 


	meta = soup.find("meta", property="og:url")
	if meta: 
		if meta['content'].startswith("http://allrecipes.com") :
			return getServingSizeAllRecipes(soup)
		elif meta['content'].startswith("http://www.foodnetwork.com") : 
			return getIngredientsFoodNetwork(soup)
	print "UNKNOWN WEBSITE, PLEASE ADD!"
	return []


def getSteps(url) :

    
    meta = soup.find("meta", property="og:url")
    if meta: 
        if meta['content'].startswith("http://allrecipes.com") :
            return getStepsAllRecipes(soup)
        elif meta['content'].startswith("http://www.foodnetwork.com") : 
            return getIngredientsFoodNetwork(htm)
    print "UNKNOWN WEBSITE, PLEASE ADD!"
    return []

for p in range(1):
    url = allrecipesexample + str(p + 1)
    sock = urllib.urlopen(url)
    # read from the web server
    html = sock.read()
    # close connection to the web server
    sock.close()
    # parse read html
    soup = BeautifulSoup(html, "html.parser")

    recipes = soup.find_all("a", attrs={'data-internal-referrer-link': "search result"})

    print recipes
    for r in recipes:  
        if r['href'][:7] == "/recipe":
            if not r['href'] in allrecipes: 
                allrecipes.append(r["href"])
                print r["href"]

    time.sleep(0.5)

print allrecipes


with open("out.csv", "wb") as outfile:
	fieldnames = ["url", "name", "rating", "serving_size", "cooking_time", "ingredients", "steps"]
 	writer = csv.DictWriter(outfile, fieldnames=fieldnames)
 	writer.writeheader()


	for recipe in allrecipes :
	    # open the web url
	    sock = urllib.urlopen("http://allrecipes.com" + recipe)
	    # read from the web server
	    html = sock.read()
	    # close connection to the web server
	    sock.close()
	    # parse read html
	    soup = BeautifulSoup(html, "html.parser")
	    writer.writerow({
	    	"url": "http://allrecipes.com" + recipe, 
	    	"name": getName(soup), 
	    	"rating": getRating(soup),
	    	"serving_size": getServingSize(soup),
	    	"cooking_time": getCookTime(soup),
	    	"ingredients": getIngredients(soup),
	    	"steps": getSteps(soup)
	    })
	    
time.sleep(0.5)