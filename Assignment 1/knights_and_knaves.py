#written by peizhi ouyang 
#z5191764


import sys
import copy
import os
import re
import itertools

# Read the document
file_name = input('Which text file do you want to use for the puzzle? ')

try:
    with open(file_name,'r',encoding='utf_8') as file:
        data = file.read()
        #Rule out no data
        if data == '':
            print('Incorrect file.')
        data = data.replace('\n',' ')       
except ValueError or IOError:
    print('Incorrect file.')
    sys.exit()

# name find
# remove all punctuation marks and divide every word,then select the useful names,



module = copy.deepcopy(data)
data = re.split(r'[?!.]', data)
D_name = []
for text in data:
    # remove all ?!.,;" and use space to fill it
    text = text.replace(',',' ')
    text = text.replace(':',' ')
    text = text.replace('"',' ')
    text = text.split()
    for m in range(len(text)):
        # 1.we can find the name behind the 'Sir'
		# 2.when it is 'Sirs',the name are the words behind 'Sirs' and behind the 'and' 
        if text[m] == 'Sir':
            D_name.append(text[m+1])
        if text[m] == 'Sirs':
            i = m
            while 1:
                i = i + 1
                if text[i] != 'and':
                    D_name.append(text[i])
                if text[i] == 'and':
                    D_name.append(text[i+1])
                    break
if D_name[0] == ' ':
    del D_name[0]
# we remove repeated names and sorted it by the string lower sequence
D_name = sorted(D_name, key=str.lower)
Aname = []
for i in D_name:
    if not i in Aname:
        Aname.append(i)
print('The Sirs are: ',end='')
#Aname.lstrip（）
for i in Aname:
    print(i, end = ' ')
print()


#find all the combinations 
#find the words talked by hte knight or knave
#change knight/knave to 1/0
#find the speaker
#combine the combinations and 1/0 and get the all situations
#match all the situations
#list all 8 words and turn to 16 cases
assumption = {}
from itertools import combinations
for i in range(0,len(Aname)+1):
    assumption[i] = []
    do_L = []
    #find all the combinations 
    temp = combinations(Aname,i)
    do_L = list(temp)
    for x in do_L:
        assumption[i].append(x)


module = module.replace('!"','"!')
module = module.replace('."','".')
module = module.replace('?"','"?')
module = re.split(r'[?!.]', module)
speaker = {}
#divide the whole sentense to the single words
for line in module:
    line = line.replace(',','')
    line = line.replace(':','')
    line = line.replace('"',' _ ')
    line = line.split()
    # eliminate all the marks without " 
	#and turn the " to a unique mark
    temp = ''
    words = []
    for i in range(len(line)-2):
        if line[i] == '_':
            a = i
            z = i
            while 1:
                z = z + 1
                if line[z] != '_':
                    temp += ' '+ line[z]
                if line[z] == '_' :
                    b = z
                    words.append(temp)
                    for ls in words:
                        ls = ls.split()
                    for y in range(len(line)):
                        if y < a or y > b:
                            if line[y] == 'Sir':
                                speaker.setdefault(line[y+1], []).append(ls)
                    del line[a]
                    del line[b-1]
                    break
                    


Lname = copy.deepcopy(Aname)
# define a Boolean to know the true or false
# true can be seen as 1
# false can be seen as 0
class Boolean(object):
    def __init__(self,name,value = 0):
        self.name = name
        self.value = value
        self.state = False 
        if value == 0:
            self.state = False
        if value == 1:
            self.state = True
for i in range(len(Lname)):
    Lname[i] = Boolean(Aname[i])

# combine the combinations and 1/0 and get the all situations
# bulid a dict to record
# if 3 which means 000 001 010 100 011 101 110 111 totully 8 cases

allcase = {}
#possible case
case = copy.deepcopy(assumption)
for key in case:
    allcase[key] = []
    for i in case[key]:
        L_knight = []
        for x in i:
            L_knight.append(x)
        Standard = copy.deepcopy(Lname)
        for k in Standard:
            if k.name in L_knight:
                k.state = True
        allcase[key].append(Standard)


#match all the situations
L_comb = []
for key in allcase:
    for i in allcase[key]:
        temp = []
        for j in range(len(Aname)):
            temp.append((i[j].name,i[j].state))
        L_comb.append(temp)

#list all 8 words and turn to 16 cases
# define the condition which sentences should into which cycle 
# can be divide 2 case which is knight and kanve

def condition(key, Standard, words, S_name):

    #1, at least.+I am.+Sir XXX or Sir XXX is a .
    #words is true = 1+ true
    if 'least' in words or 'or' in words or 'am' in words:
        for i in Standard:
            for j in S_name:
                if 'Knight' in words and i[0] == j and i[1] == True:
                    return True                   
                if 'Knave' in words and i[0] == j and i[1] == False:
                    return True

    #2, at most.
    # the words is true = 0 true or 1 true
    if 'most' in words and 'Knight' in words:
        temp = []
        for i in Standard:
            for j in S_name:
                if i[0] == j and i[1] == True:
                    temp.append(j)
        if len(temp) <= 1:
            return True
    if 'most' in words and 'Knave' in words:
        temp = []
        for i in Standard:
            for j in S_name:
                if i[0] == j and i[1] == False:
                    temp.append(j)
        if len(temp) <= 1:
            return True
        
    #3, exactly/Exactly.
    # words true = only 1 true      
    if 'exactly' in words or 'Exactly' in words:
        if 'Knight' in words:
            temp = []
            for i in Standard:
                for j in S_name:
                    if i[0] == j and i[1] == True:
                        temp.append(j)
            if len(temp) == 1:
                return True
    if 'exactly' in words or 'Exactly' in words:
        if 'Knave' in words:
            temp = []
            for i in Standard:
                for j in S_name:
                    if i[0] == j and i[1] == False:
                        temp.append(j)
            if len(temp) == 1:
                return True

    #4, all/All. + Sir XXX and Sir XXX are 
    #words true = all people in words are true 
    if 'Knights' in words:
        temp = []
        for i in Standard:
            for j in S_name:
                if i[0] == j and i[1] == True:
                    temp.append(j)
        if len(temp) == len(S_name):
            return True
    if 'Knaves' in words:
        temp = []
        for i in Standard:
            for j in S_name:
                if i[0] == j and i[1] == False:
                    temp.append(j)
        if len(temp) == len(S_name):
            return True

    #5, I am.
    # only 1 person 
    # if the person is true and the words is true
	# it is impoosible that 'i am Knave'
	#can be combined with 1 and 7

    #6, Sir XXX is a.
    # as the name in speakername is true the words is true
    if words[0] == 'Sir' and words[2] == 'is':
        if 'Knight' in words:
            for i in Standard:
                for j in S_name:
                    if i[0] == j and i[1] == True:
                        return True
    if words[0] == 'Sir' and words[2] == 'is':
        if 'Knave' in words:
            for i in Standard:
                for j in S_name:
                    if i[0] == j and i[1] == False:
                        return True

    #7, Sir XXX or Sir XXX is a .
    # speakername has 1 true ,the words is true
	# the same as 1


    #8, Sir XXX and Sir XXX are 
    # the speakername should be all true the words can be true
	# the same as 4, it claim that all of the people in this words are true/false

    return False
    # other situation can not be achieve

Final = []
S_name = []
Num = 0
for key in speaker.keys():
    Num += len(speaker[key])
# To judge, If the match is right, knight must have said it; if it is wrong, knave must have said it
#Other scenarios suggest that is not the solution
for i in L_comb:
    Standard = i
    temp = []
    for key in speaker:
        for value in speaker[key]:
            words = value
            # find all mentioned name in one claim
            # if thw words has 'i',should add the speaker if the words has 'us',should add all the people in the text
            S_name = []
            if 'us' in words:
                S_name = Aname
            if 'I' in words:
                S_name.append(key)
            for i in range(len(words)):
                if words[i] == 'Sir':
                    S_name.append(words[i+1])
            for j in Standard:
                if j[0] == key and condition(key, Standard, words, S_name) == True and j[1] == True:
                    temp.append(Standard)
                if j[0] == key and condition(key, Standard, words, S_name) == False and j[1] == False:
                    temp.append(Standard)
    # a right result is that it needs to meet all the criteria
    # And then we use the for loop to figure out how many of these are true
    if len(temp)==Num:
        Final.append(Standard)
#print
if len(Final) > 1:
    print('There are {} solutions.'.format(len(Final)))
elif len(Final)==1:
    print('There is a unique solution:')
    for i in Final:
        for j in i:
            if j[1] == True:
                print('Sir {} is a Knight.'.format(j[0]))
            if j[1] == False:
                print('Sir {} is a Knave.'.format(j[0]))
else:
    print('There is no solution.')                