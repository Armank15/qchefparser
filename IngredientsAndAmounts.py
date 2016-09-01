
def foobar(str) :

	units = ['cups', 'teaspoons', 'teaspoon', 'cup', 'tablespoons', 'tablespoon', 'ounces', 'pound', 'pounds', 'ounce']


	result = {}

	a = str.split(" ")
	from fractions import Fraction
	try :
		result['quantity'] = float(Fraction(a[0]))
	except :
		print "Error: I only handle floats"
		return None
	if a[1] in units :
		result['unit'] = a[1]
		result['ingredient'] = ' '.join(a[2:])
	else :
		result['ingredient'] = ' '.join(a[1:])
	return result




tests = [u'1 pound sweet Italian sausage', 
		 u'3/4 pound lean ground beef', 
		 u'1/2 cup minced onion', 
		 u'2 cloves garlic, crushed', 
		 u'1 (28 ounce) can crushed tomatoes', 
		 u'2 (6 ounce) cans tomato paste', 
		 u'2 (6.5 ounce) cans canned tomato sauce', 
		 u'1/2 cup water', 
		 u'2 tablespoons white sugar', 
		 u'1 1/2 teaspoons dried basil leaves', 
		 u'1/2 teaspoon fennel seeds', 
		 u'1 teaspoon Italian seasoning', 
		 u'1 tablespoon salt', 
		 u'1/4 teaspoon ground black pepper', 
		 u'4 tablespoons chopped fresh parsley', 
		 u'12 lasagna noodles', 
		 u'16 ounces ricotta cheese', 
		 u'1 egg', 
		 u'1/2 teaspoon salt', 
		 u'3/4 pound mozzarella cheese, sliced', 
		 u'3/4 cup grated Parmesan cheese'
]

for test in tests:
	print test
	print foobar(test)
