from bs4 import BeautifulSoup
from fractions import Fraction
import csv, sys, urllib, time 

# These are some example websites
allrecipesexample = "http://allrecipes.com/recipes/?grouping=all"
#"http://allrecipes.com/search/results/?wt=chicken&sort=re"


def getIngredientsAllRecipes(soup) :
	results = [ ]

	list_1 = soup.find("ul", id="lst_ingredients_1")
	list_2 = soup.find("ul", id="lst_ingredients_2")

	spans = list_1.find_all("span", class_="recipe-ingred_txt added") 
	spans2 = list_2.find_all("span", class_="recipe-ingred_txt added")

	combinedspan = spans + spans2
	for ing in combinedspan:
		results.append(ing.contents[0])
	return results

def interpretIngredients(str) :

    units = ['cups', 'teaspoons', 'teaspoon', 'cup', 'tablespoons', 'tablespoon', 'ounces', 'pound', 'pounds', 'ounce', 'cloves']

    #setup
    result = {}

    a = str.split(" ")
    result['quantity'] = ""
    result['unit'] = ""
    result['ingredient'] = ""

    #Put the right stuff in these three variables    
    unit_index = 0
    while unit_index < len(a)-1 and a[unit_index] not in units:
        unit_index += 1
    result['quantity'] = " ".join(a[:unit_index])
    result['unit'] = a[unit_index]
    result["ingredient"] = " ".join(a[unit_index+1:])
        
    #Convert the qty using fraction
    try :
        result['quantity'] = float(Fraction(result['quantity']))
    except :
        print "  Error: I only handle floats, but I got",result['quantity'],"instead!"
        return None
    return result


def getNameAllRecipes(soup) :
	results = [ ]
	name = soup.find("h1", itemprop="name")
	return name.contents


def getCookTimeAllRecipes(soup) :
	CookTime = soup.find("span", class_="ready-in-time")
	if CookTime is not None:
		return CookTime.contents
	else:
		return "-"


	#soup.find()

def getRatingAllRecipes(soup) : 

	ratingStars = soup.find("div", class_="rating-stars")

	return float(ratingStars['data-ratingstars']) 


def getStepsAllRecipes(soup) : 

	results = [ ]
	#soup = BeautifulSoup(html, "html.parser")
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


def getSteps(soup) :
    meta = soup.find("meta", property="og:url")
    if meta: 
        if meta['content'].startswith("http://allrecipes.com") :
            return getStepsAllRecipes(soup)
        elif meta['content'].startswith("http://www.foodnetwork.com") : 
            return getIngredientsFoodNetwork(htm)
    print "UNKNOWN WEBSITE, PLEASE ADD!"
    return []

def getRecipes(parent, pages, startpage=0, debug=False) :


	allrecipes = []

	for p in range(startpage,startpage+pages):
		url = parent + "&page=" + str(p + 1)
		sock = urllib.urlopen(url)
	    # read from the web server
		html = sock.read()
	    # close connection to the web server
		sock.close()
	    # parse read html
		soup = BeautifulSoup(html, "html.parser")

		recipes = soup.find_all("a", attrs={'data-internal-referrer-link': "hub recipe"})

		if debug:
			print recipes
		for r in recipes: 
			url = r.get("href") 
			if url[:7] == "/recipe" :
				if not url in allrecipes: 
					allrecipes.append(url)
	                

		time.sleep(0.5)

	if debug:
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
		    	"ingredients": [interpretIngredients(ing) for ing in getIngredients(soup)],
		    	"steps": getSteps(soup)
		    })
		    
	time.sleep(0.5)

#Can delete this
'''
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
'''
#-----------------------------------------

getRecipes(allrecipesexample,1, startpage=100)

'''
#Can delete this stuff
sock = urllib.urlopen(allrecipesexample)  
html = sock.read()
sock.close()
GetCategories(html)
'''