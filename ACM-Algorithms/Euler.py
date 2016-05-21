1)
sum = 0
for i in range(1,1000):
    if ((i%3 == 0) or (i%5 == 0)):
        sum+=i
print sum
      

2)	  
prev = 0
aux = 0        
fibonacci = 1
sum = 0
while fibonacci < 4000000:
    if(fibonacci%2 == 0):
        sum+=fibonacci
    aux = fibonacci
    fibonacci = fibonacci + prev
    prev = aux

print sum


	
4)
import math
import operator


def is_palindrome(number):
    aux = int(str(number)[::-1])
    if number == aux: return True
    else: return False

def is_prime(number):
    for i in range(2, math.trunc(math.sqrt(number))+1):
        if number%i == 0:
            return False
    return True
    
def prime_factors(number):
    factorlist=[]
    loop=2
    while loop<=number:
        if number%loop==0:
            number/=loop
            factorlist.append(loop)
        else:
            loop+=1
    return factorlist

def check_factors_boundaries(factor_list):
    aux_list = []
    boundary_pass = False
    for j in factor_list:
        if j > 999:
            boundary_pass = True            
        elif j > 100:
            continue
        else:            
            aux_list.append(j)
    group = reduce(operator.mul, aux_list, 1)
    print aux_list
    print "Multicacion " + str(group)
    if (group > 999) or (group < 100):
        boundary_pass = True    
    return boundary_pass

top = 999*999
bottom = 100*100
while top > bottom:    
    i = top
    while i > bottom:
        if is_palindrome(i):
            break        
        i -= 1
    print i
        
    if check_factors_boundaries(prime_factors(i)):
        top = i - 1
    else:
        break

print prime_factors(i)


5)
import math
import operator
    
def prime_factors(number):
    factorlist=[]
    loop=2
    while loop<=number:
        if number%loop==0:
            number/=loop
            factorlist.append(loop)
        else:
            loop+=1
    return factorlist

def find_max_divisor(_from, _to, number):
    for i in xrange(_to, _from, -1):
        if number%i == 0:
            return i
    return 1

bottom = 1  
top = 20       
aux = 1
for i in range(bottom,top):
    aux = aux * i
        
print "Max number: " +  str(aux)
factors = prime_factors(aux)
exponent_list = []
minor_list = []
for i in range (1, len(factors)):
    exponent_list.append(factors.count(i))
    if exponent_list[i-1] != 0:
            minor_list.append(pow(i,exponent_list[i-1]))

result_list = []
for i in minor_list:
    if i > top:
        result_list.append(find_max_divisor(bottom, top, i))
    else:
        result_list.append(i)
        
print "Reduced but evenly divisible by all of the numbers: " + str(result_list)
print "Final Result: "+ str(reduce(operator.mul, result_list, 1))

6)
import math
    
def sum_square_difference(bottom, top):
    aux = 0
    sum = 0
    for i in range(bottom,top + 1):
        aux = aux + math.pow(i,2)
        sum = sum + i
        
    square_sum = math.pow(sum,2)
    #print aux
    #print square_sum
    diference = square_sum - aux
    return diference  
            
def sum_square_difference_optimized(bottom,top):
    aux = 0
    for i in range(bottom,top + 1):
        aux = aux + math.pow(i,2)
        
    square_sum = math.pow(top * (top+1)/2,2)
    #print aux
    #print square_sum
    diference = square_sum - aux
    return diference  

print sum_square_difference(1,100)       
print sum_square_difference_optimized(1,100)


7)
import math
    
def is_prime(number):
    for i in range(2, math.trunc(math.sqrt(number))+1):
        if number%i == 0:
            return False
    return True

def n_prime(n):
    i = 0
    while n > 0:
        i += 1
        if is_prime(i):        
            n -= 1
    return i
    
print n_prime(10001)


8)

V = [7,3,1,6,7,1,7,6,5,3,1,3,3,0,6,2,4,9,1,9,2,2,5,1,1,9,6,7,4,4,2,6,5,7,4,7,4,2,3,5,5,3,4,9,1,9,4,9,3,4,9,6,9,8,3,5,2,0,3,1,2,7,7,4,5,0,6,3,2,6,2,3,9,5,7,8,3,1,8,0,1,6,9,8,4,8,0,1,8,6,9,4,7,8,8,5,1,8,4,3,8,5,8,6,1,5,6,0,7,8,9,1,1,2,9,4,9,4,9,5,4,5,9,5,0,1,7,3,7,9,5,8,3,3,1,9,5,2,8,5,3,2,0,8,8,0,5,5,1,1,1,2,5,4,0,6,9,8,7,4,7,1,5,8,5,2,3,8,6,3,0,5,0,7,1,5,6,9,3,2,9,0,9,6,3,2,9,5,2,2,7,4,4,3,0,4,3,5,5,7,6,6,8,9,6,6,4,8,9,5,0,4,4,5,2,4,4,5,2,3,1,6,1,7,3,1,8,5,6,4,0,3,0,9,8,7,1,1,1,2,1,7,2,2,3,8,3,1,1,3,6,2,2,2,9,8,9,3,4,2,3,3,8,0,3,0,8,1,3,5,3,3,6,2,7,6,6,1,4,2,8,2,8,0,6,4,4,4,4,8,6,6,4,5,2,3,8,7,4,9,3,0,3,5,8,9,0,7,2,9,6,2,9,0,4,9,1,5,6,0,4,4,0,7,7,2,3,9,0,7,1,3,8,1,0,5,1,5,8,5,9,3,0,7,9,6,0,8,6,6,7,0,1,7,2,4,2,7,1,2,1,8,8,3,9,9,8,7,9,7,9,0,8,7,9,2,2,7,4,9,2,1,9,0,1,6,9,9,7,2,0,8,8,8,0,9,3,7,7,6,6,5,7,2,7,3,3,3,0,0,1,0,5,3,3,6,7,8,8,1,2,2,0,2,3,5,4,2,1,8,0,9,7,5,1,2,5,4,5,4,0,5,9,4,7,5,2,2,4,3,5,2,5,8,4,9,0,7,7,1,1,6,7,0,5,5,6,0,1,3,6,0,4,8,3,9,5,8,6,4,4,6,7,0,6,3,2,4,4,1,5,7,2,2,1,5,5,3,9,7,5,3,6,9,7,8,1,7,9,7,7,8,4,6,1,7,4,0,6,4,9,5,5,1,4,9,2,9,0,8,6,2,5,6,9,3,2,1,9,7,8,4,6,8,6,2,2,4,8,2,8,3,9,7,2,2,4,1,3,7,5,6,5,7,0,5,6,0,5,7,4,9,0,2,6,1,4,0,7,9,7,2,9,6,8,6,5,2,4,1,4,5,3,5,1,0,0,4,7,4,8,2,1,6,6,3,7,0,4,8,4,4,0,3,1,9,9,8,9,0,0,0,8,8,9,5,2,4,3,4,5,0,6,5,8,5,4,1,2,2,7,5,8,8,6,6,6,8,8,1,1,6,4,2,7,1,7,1,4,7,9,9,2,4,4,4,2,9,2,8,2,3,0,8,6,3,4,6,5,6,7,4,8,1,3,9,1,9,1,2,3,1,6,2,8,2,4,5,8,6,1,7,8,6,6,4,5,8,3,5,9,1,2,4,5,6,6,5,2,9,4,7,6,5,4,5,6,8,2,8,4,8,9,1,2,8,8,3,1,4,2,6,0,7,6,9,0,0,4,2,2,4,2,1,9,0,2,2,6,7,1,0,5,5,6,2,6,3,2,1,1,1,1,1,0,9,3,7,0,5,4,4,2,1,7,5,0,6,9,4,1,6,5,8,9,6,0,4,0,8,0,7,1,9,8,4,0,3,8,5,0,9,6,2,4,5,5,4,4,4,3,6,2,9,8,1,2,3,0,9,8,7,8,7,9,9,2,7,2,4,4,2,8,4,9,0,9,1,8,8,8,4,5,8,0,1,5,6,1,6,6,0,9,7,9,1,9,1,3,3,8,7,5,4,9,9,2,0,0,5,2,4,0,6,3,6,8,9,9,1,2,5,6,0,7,1,7,6,0,6,0,5,8,8,6,1,1,6,4,6,7,1,0,9,4,0,5,0,7,7,5,4,1,0,0,2,2,5,6,9,8,3,1,5,5,2,0,0,0,5,5,9,3,5,7,2,9,7,2,5,7,1,6,3,6,2,6,9,5,6,1,8,8,2,6,7,0,4,2,8,2,5,2,4,8,3,6,0,0,8,2,3,2,5,7,5,3,0,4,2,0,7,5,2,9,6,3,4,5,0]


#window of 5 - w represents the position of the last digit of the window in V

greatest = 0
max_w = 5


def product(j):
    result = 1
    for i in range (1,max_w + 1):
        result *= V[j-i]
    return result

def slide(position):
    count = 0
    while count != max_w and position < len(V):
        if V[position] != 0:
            count += 1
        else:
            count = 0
        position += 1
    return position

w = slide(0)
while w < len(V):
    prod = product(w)    
    if prod > greatest:
        greatest = prod
    if V[w+1] == 0:
        w = slide(w)
    else:
        w += 1
print greatest

9)

import math




10)

import math
def is_prime(number):
    for i in range(2, math.trunc(math.sqrt(number))+1):
        if number%i == 0:
            return False
    return True

prime_sum = 0
for i in range(2,2000000):
    if is_prime(i):
        prime_sum += i
print prime_sum


11)

import math

M = [[ 8, 02, 22, 97, 38, 15, 00, 40, 00, 75, 04, 05, 07, 78, 52, 12, 50, 77, 91, 8],
[49, 49, 99, 40, 17, 81, 18, 57, 60, 87, 17, 40, 98, 43, 69, 48, 04, 56, 62, 00],
[81, 49, 31, 73, 55, 79, 14, 29, 93, 71, 40, 67, 53, 88, 30, 03, 49, 13, 36, 65],
[52, 70, 95, 23, 04, 60, 11, 42, 69, 24, 68, 56, 01, 32, 56, 71, 37, 02, 36, 91],
[22, 31, 16, 71, 51, 67, 63, 89, 41, 92, 36, 54, 22, 40, 40, 28, 66, 33, 13, 80],
[24, 47, 32, 60, 99, 03, 45, 02, 44, 75, 33, 53, 78, 36, 84, 20, 35, 17, 12, 50],
[32, 98, 81, 28, 64, 23, 67, 10, 26, 38, 40, 67, 59, 54, 70, 66, 18, 38, 64, 70],
[67, 26, 20, 68, 02, 62, 12, 20, 95, 63, 94, 39, 63, 8, 40, 91, 66, 49, 94, 21],
[24, 55, 58, 05, 66, 73, 99, 26, 97, 17, 78, 78, 96, 83, 14, 88, 34, 89, 63, 72],
[21, 36, 23, 9, 75, 00, 76, 44, 20, 45, 35, 14, 00, 61, 33, 97, 34, 31, 33, 95],
[78, 17, 53, 28, 22, 75, 31, 67, 15, 94, 03, 80, 04, 62, 16, 14, 9, 53, 56, 92],
[16, 39, 05, 42, 96, 35, 31, 47, 55, 58, 88, 24, 00, 17, 54, 24, 36, 29, 85, 57],
[86, 56, 00, 48, 35, 71, 89, 07, 05, 44, 44, 37, 44, 60, 21, 58, 51, 54, 17, 58],
[19, 80, 81, 68, 05, 94, 47, 69, 28, 73, 92, 13, 86, 52, 17, 77, 04, 89, 55, 40],
[04, 52, 9, 83, 97, 35, 99, 16, 07, 97, 57, 32, 16, 26, 26, 79, 33, 27, 98, 66],
[88, 36, 68, 87, 57, 62, 20, 72, 03, 46, 33, 67, 46, 55, 12, 32, 63, 93, 53, 69],
[04, 42, 16, 73, 38, 25, 39, 11, 24, 94, 72, 18, 8, 46, 29, 32, 40, 62, 76, 36],
[20, 69, 36, 41, 72, 30, 23, 88, 34, 62, 99, 69, 82, 67, 59, 85, 74, 04, 36, 16],
[20, 73, 35, 29, 78, 31, 90, 01, 74, 31, 49, 71, 48, 86, 81, 16, 23, 57, 05, 54],
[01, 70, 54, 71, 83, 51, 54, 69, 16, 92, 33, 48, 61, 43, 52, 01, 89, 19, 67, 48] ]

max_wnd = 4
greatest = 0

def get_diag_225(i,j):
    result = 1
    try:
        for k in range (0, max_wnd):
            result *= M[i+k][j-k]
    except:
        result = 0
    return result

def get_diag_315(i,j):
    result = 1
    try:
        for k in range (0, max_wnd):
            result *= M[i+k][j+k]
    except:
        result = 0
    return result

def get_horizontal(i,j):
    result = 1
    try:
        for k in range (0, max_wnd):
            result *= M[i][j+k]
    except:
        result = 0
    return result

def get_vertical(i,j):
    result = 1
    try:
        for k in range (0, max_wnd):
            result *= M[i+k][j]
    except:
        result = 0
    return result

for row in range(0, len(M)):
    for col in range(0, len(M)):       
        value = get_diag_225(row,col)
        if value > greatest:
            greatest = value
        value = get_diag_315(row,col)
        if value > greatest:
            greatest = value
        value = get_horizontal(row,col)
        if value > greatest:
            greatest = value
        value = get_vertical(row,col)
        if value > greatest:
            greatest = value
            
print greatest          



12)

import math

def get_divisors(n):
	divisores = []
	for i in range(1,int(math.ceil(math.sqrt(n)))):
		if n % i == 0:
			divisores.append(i)
			if i != n/i:
				divisores.append(n/i)
        return divisores

sumatoria = 0
for i in range(1,100000):
    sumatoria += i
    div = get_divisors(sumatoria)
    if len(div) > 500:
        print sumatoria
	break
print div



13)

data = """37107287533902102798797998220837590246510135740250463769376774900097126481248969700780504170182605387432498619952474105947423330951305812372661730962991942213363574161572522430563301811072406154908250230675882075393461711719803104210475137780632466768926167069662363382013637841838368417873436172675728112879812849979408065481931592621691275889832738442742289174325203219235894228767964876702721893184745144573600130643909116721685684458871160315327670386486105843025439939619828917593665686757934951621764571418565606295021572231965867550793241933316490635246274190492910143244581382266334794475817892575867718337217661963751590579239728245598838407582035653253593990084026335689488301894586282278288018119938482628201427819413994056758715117009439035398664372827112653829987240784473053190104293586865155060062958648615320752733719591914205172558297169388870771546649911559348760353292171497005693854370070576826684624621495650076471787294438377604532826541087568284431911906346940378552177792951453612327252500029607107508256381565671088525835072145876576172410976447339110607218265236877223636045174237069058518606604482076212098132878607339694128114266041808683061932846081119106155694051268969251934325451728388641918047049293215058642563049483624672216484350762017279180399446930047329563406911573244438690812579451408905770622942919710792820955037687525678773091862540744969844508330393682126183363848253301546861961243487676812975343759465158038628759287849020152168555482871720121925776695478182833757993103614740356856449095527097864797581167263201004368978425535399209318374414978068609844840309812907779179908821879532736447567559084803087086987551392711854517078544161852424320693150332599594068957565367821070749269665376763262354472106979395067965269474259770973916669376304263398708541052684708299085211399427365734116182760315001271653786073615010808570091499395125570281987460043753582903531743471732693212357815498262974255273730794953759765105305946966067683156574377167401875275889028025717332296191766687138199318110487701902712526768027607800301367868099252546340106163286652636270218540497705585629946580636237993140746255962240744869082311749777923654662572469233228109171419143028819710328859780666976089293863828502533340334413065578016127815921815005561868836468420090470230530811728164304876237919698424872550366387845831148769693215490281042402013833512446218144177347063783299490636259666498587618221225225512486764533677201869716985443124195724099139590089523100588229554825530026352078153229679624948164195386821877476085327132285723110424803456124867697064507995236377742425354112916842768655389262050249103265729672370191327572567528565324825826546309220705859652229798860272258331913126375147341994889534765745501184957014548792889848568277260777137214037988797153829820378303147352772158034814451349137322665138134829543829199918180278916522431027392251122869539409579530664052326325380441000596549391598795936352974615218550237130764225512118369380358038858490341698116222072977186158236678424689157993532961922624679571944012690438771072750481023908955235974572318970677254791506150550495392297953090112996751986188088225875314529584099251203829009407770775672113067397083047244838165338735023408456470580773088295917476714036319800818712901187549131054712658197623331044818386269515456334926366572897563400500428462801835170705278318394258821455212272512503275512160354698120058176216521282765275169129689778932238195734329339946437501907836945765883352399886755061649651847751807381688378610915273579297013376217784275219262340194239963916804498399317331273132924185707147349566916674687634660915035914677504995186714302352196288948901024233251169136196266227326746080059154747183079839286853520694694454072476841822524674417161514036427982273348055556214818971426179103425986472045168939894221798260880768528778364618279934631376775430780936333301898264209010848802521674670883215120185883543223812876952786713296124747824645386369930090493103636197638780396218407357239979422340623539380833965132740801111666627891981488087797941876876144230030984490851411606618262936828367647447792391803351109890697907148578694408955299065364044742557608365997664579509666024396409905389607120198219976047599490197230297649139826800329731560371200413779037855660850892521673093931987275027546890690370753941304265231501194809377245048795150954100921645863754710598436791786391670211874924319957006419179697775990283006991536871371193661495281130587638027841075444973307840789923115535562561142322423255033685442488917353448899115014406480203690680639606723221932041495354150312888033953605329934036800697771065056663195481234880673210146739058568557934581403627822703280826165707739483275922328459417065250945123252306082291880205877731971983945018088807242966198081119777158542502016545090413245809786882778948721859617721078384350691861554356628840622574736922845095162084960398013400172393067166682355524525280460972253503534226472524250874054075591789781264330331690"""

n = 50
numbers = [data[i:i+n] for i in range(0, len(data), n)]

numbers = map(int, numbers)
result = sum(numbers)
print result
print "First ten digits:"
print str(result)[:10]


14)

def procedure1(n):
    return n/2

def procedure2(n):
    return 3*n + 1

def collatz(n):
    sequence = []
    while n != 1:
        sequence.append(n)
        if n%2 == 0:
            n = procedure1(n)
        else:
            n = procedure2(n)
    return sequence

def find_longest_chain(start, end):
    longest_chain = 0
    max_n = 0
    for i in range(start,end+1):
        chain = collatz(i)
        if len(chain) > longest_chain:
            longest_chain = len(chain)
            max_n = i
    return (max_n, longest_chain)

print find_longest_chain(1,1000000)



15)

def pascalTriangle(n): 
    # Caso base 
    if n == 0: 
        return [] 
     
    if n == 1: 
        return [[1]] 
     
    # Caso recursivo 
    last_list = pascalTriangle(n-1) 
     
    this_list = [1] 
    for i in range(1, n-1): 
        this_list.append(last_list[n-2][i-1] + last_list[n-2][i]) 
    this_list.append(1) 
     
    last_list.append(this_list) 
     
    return last_list 
     
def lastLine(n): 
    triangle = pascalTriangle(n) 
    return triangle[n-1]

max(pascalTriangle(40+1)[40])

16)

import math

number = '{0:.0f}'.format(math.pow(2,1000))
result = 0
print number
for i in range(0,len(number)):
    result += int(number[i])
    
print result
	
	
17)

def convert_unity(n):
    n = int(n)
    if n==1:
        return "one"
    elif n==2:
        return "two"
    elif n==3:
        return "three"
    elif n==4:
        return "four"
    elif n==5:
        return "five"
    elif n==6:
        return "six"
    elif n==7:
        return "seven"
    elif n==8:
        return "eight"
    elif n==9:
        return "nine"
    else: #equals 0
        return ""

def convert_dec(n):
    n = int(n)
    if n==10:
        return "ten"
    elif n==11:
        return "eleven"
    elif n==12:
        return "twelve"
    elif n==13:
        return "thirteen"
    elif n==14:
        return "fourteen"
    elif n==15:
        return "fifteen"
    elif n==16:
        return "sixteen"
    elif n==17:
        return "seventeen"
    elif n==18:
        return "eighteen"
    elif n==19:
        return "nineteen"
    elif n==2:
        return "twenty-"
    elif n==3:
        return "thirty-"
    elif n==4:
        return "forty-"
    elif n==5:
        return "fifty-"
    elif n==6:
        return "sixty-"
    elif n==7:
        return "seventy-"
    elif n==8:
        return "eighty-"
    elif n==9:
        return "ninety-"
    else: #equals 0
        return "" 

def convert_cent(n):
    n = int(n)
    return convert_unity(n) + " hundred"
 
def convert_mil(n):
    return "one thousand"

def convert_to_letters(n):
    letters = ""
    length = len(str(n))
    if length == 4:
        letters = convert_mil(n)
    elif length == 3:
        if  str(n)[1] == '0' and str(n)[2] == '0':            
            return convert_cent(str(n)[0])        
        if str(n)[0] == '1':
            letters += convert_cent(1)
        else:
            letters += convert_cent(str(n)[0])       
            
        if str(n)[1] != 0 or str(n)[2] != 0:
            if str(n)[1] == '1':
                letters += " and " + convert_dec(str(n)[1]+str(n)[2])
            else:
                letters += " and " + convert_dec(str(n)[1]) + convert_unity(str(n)[2])
    elif length == 2:
        if str(n)[0] == '1':
            letters += convert_dec(str(n))
        else:
            letters += convert_dec(str(n)[0]) + convert_unity(str(n)[1])
    else:
        letters = convert_unity(str(n)[0])
        
    return letters

words = ""
for i in range(1,1000+1):
    words += convert_to_letters(i)
    
words = words.split(" ")

words = "".join(words).split("-")
words = "".join(words)
print words
print len(words)



18) 67)

#include <iostream>
#include <cstdlib>

using namespace std;

int triangle[100][100];
int N;

int max(int a, int b)
{
    if (a > b) return a;
    return b;
}

int path(int i, int j)
{
    if (i == N) return triangle[i][j];
	else
	  return max(triangle[i+1][j], triangle[i+1][j+1]) + triangle[i][j];
 }

int main() {
    int tmp = 0;
    cin >> N;
    for (int i=0; i<N; i++)
    {
        for(int j=0; j <=i; j++) { 
                scanf("%d", &tmp);
                triangle[i][j] = tmp;          
        }
    }            
    fflush(stdin);
    
   for (int i = N-1; i >=0; i--)
	for(int j = 0; j <= i; j++)
		triangle[i][j] = path(i,j);     
    
    cout << endl;
    for (int i=0; i<N; i++)
    {
        for(int j=0; j <=i; j++)
          cout << triangle[i][j] << " ";
        cout << endl;
    }       
    
    cout << endl;    
    cout << triangle[0][0] << endl;        
    getchar();
}




20)

def factorial(n):    
    if n == 1:
        return 1
    return n*factorial(n-1)

def sum_digits(n):
    result = 0
    for i in n:
        result += int(i)
    return result

print sum_digits(str(factorial(100)))


21)

import math

def is_prime(n):
    for i in range(2, math.trunc(math.sqrt(n))+1):
        if n%i == 0:
            return False
    return True

def get_divisors(n):
	divisores = []
	for i in range(1,int(math.ceil(math.sqrt(n)))):
		if n % i == 0:
			divisores.append(i)                                        
                        if i != n/i and i != 1:                                
				divisores.append(n/i)                     
        return divisores

def check_amicable(n,m):
    divisors = get_divisors(n)
    if m == sum(divisors):       
        return True
    return False

amicable = []

for b in range(4,10000+1):
    divisors = get_divisors(b)
    a = sum(divisors)
    if check_amicable(a,b) and a != b:
        amicable.append(b)

print amicable
print sum(amicable)

			
22)

import string
values = dict()
for index, letter in enumerate(string.ascii_uppercase):
   values[letter] = index + 1
def get_score(name):
    score = 0
    for c in name:
        score += values[c]
    return score    
f = open("names.txt", "r")
data = "".join(f.readlines())
data = data[1:len(data)-1]
names = data.split('","')
names = sorted(names)
result = 0
for i in range(0,len(names)):
    result += (i + 1) * get_score(names[i])
print result



25)

fibo = []

def calcFibo(n):
    if fibo[n] != -1:
        return fibo[n]
    fibo[n] = calcFibo(n-2) + calcFibo(n-1)
    return fibo[n]

for i in range(1,10000):
    fibo.append(-1)

fibo[0] = 1
fibo[1] = 1
start = 300
while len(str(calcFibo(start))) < 1000:
    start+=1

print start

