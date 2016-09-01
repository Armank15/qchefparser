from fractions import Fraction
import sys

def foobar(str) :

    units = ['cups', 'teaspoons', 'teaspoon', 'cup', 'tablespoons', 'tablespoon', 'ounces', 'pound', 'pounds', 'ounce', 'cloves']

    #setup
    result = {}
    a = str.split(" ")
    print a
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
        print "Error: I only handle floats"
        return None
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
    print
