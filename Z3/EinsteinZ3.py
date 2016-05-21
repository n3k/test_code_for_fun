'''
Let us assume that there are five houses of different colors next to each other on the same road. In each house lives a man of a different nationality. Every man has his favorite drink, his favorite brand of cigarettes, and keeps pets of a particular kind.
The Englishman lives in the red house.
The Swede keeps dogs.
The Dane drinks tea.
The green house is just to the left of the white one.
The owner of the green house drinks coffee.
The Pall Mall smoker keeps birds.
The owner of the yellow house smokes Dunhills.
The man in the center house drinks milk.
The Norwegian lives in the first house.
The Blend smoker has a neighbor who keeps cats.
The man who smokes Blue Masters drinks bier.
The man who keeps horses lives next to the Dunhill smoker.
The German smokes Prince.
The Norwegian lives next to the blue house.
The Blend smoker has a neighbor who drinks water.
The question to be answered is: Who keeps fish?
'''


from z3 import *

pallMall = Int('pallMall')
dunhills = Int('dunhills')
blueMasters = Int('blueMasters')
prince = Int('prince')
blend = Int('blend')

tea = Int('tea')
coffee = Int('coffee')
milk = Int('milk')
beer = Int('beer')
water = Int('water')

Englishman = Int('Englishman')
Swede = Int('Swede')
Dane = Int('Dane')
Norwegian = Int('Norwegian')
German = Int('German')

red = Int('red')
green = Int('green')
yellow = Int('yellow')
blue = Int('blue')
white = Int('white')

dogs = Int('dogs')
birds = Int('birds')
horses = Int('horses')
cats = Int('cats')
fish = Int('fish')

s = Solver()

# Add the constraints

s.add(pallMall>=1, pallmall<=5)
s.add(dunhills>=1, dunhills<=5)
s.add(blueMasters>=1, blueMasters<=5)
s.add(prince>=1, prince<=5)
s.add(blend>=1, blend<=5)

s.add(tea>=1, tea<=5)
s.add(coffee>=1, coffee<=5)
s.add(milk>=1, milk<=5)
s.add(beer>=1, beer<=5)
s.add(water>=1, water<=5)

s.add(Englishman>=1, Englishman<=5)
s.add(Swede>=1, Swede<=5)
s.add(Dane>=1, Dane<=5)
s.add(Norwegian>=1, Norwegian<=5)
s.add(German>=1, German<=5)

s.add(red>=1, red<=5)
s.add(green>=1, green<=5)
s.add(yellow>=1, yellow<=5)
s.add(blue>=1, blue<=5)
s.add(white>=1, white<=5)

s.add(dogs>=1, dogs<=5)
s.add(birds>=1, birds<=5)
s.add(horses>=1, horses<=5)
s.add(cats>=1, cats<=5)
s.add(fish>=1, fish<=5)

s.add(Englishman == red)
s.add(Swede == dogs)
s.add(Dane == tea)
s.add(green - 1 == white)
s.add(green == coffee)
s.add(pallMall == birds)
s.add(green == dunhills)
s.add(milk == 3)
s.add(Norwegian == 1)
s.add(Or(blend == cats + 1, blend == cats - 1))
s.add(blueMasters == beer)
s.add(Or(horses == dunhill + 1, horses == dunhill - 1))
s.add(German == prince)
s.add(Or(Norwegian == blue + 1, Norwegian == blue - 1))
s.add(Or(blend == water + 1, blend == water - 1))


print "[+] Solving..."
s.check()
ttt = s.model()
print "[MODEL---------------------------------------]"
print ttt
print "[--------------------------------------------]"