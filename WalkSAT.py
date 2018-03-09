import os
import copy
filename = os.path.dirname(os.path.abspath(__file__)) + '/input.txt';

with open(filename) as f:
    lines = f.readlines()

firstItem = lines[0]
numberOfGuests = lines[0].split(' ')[0]
numberOfTables = lines[0].split(' ')[1]

oneAssignmentFirst = []
oneAssignmentSecond = []
friendList = []
enemyList = []
symbols = []
clauses = []

#Symbols - A set of variables
for i in range(int(numberOfGuests)):
    for j in range(int(numberOfTables)):
        oneTableOne = 'X' + '_' + str(i+1) + '_' + str(j+1)
        symbols.append(oneTableOne)


#For each guest a, the assignment should be at only one table
for i in range(int(numberOfGuests)):
    oneTableOne = []
    for j in range(int(numberOfTables)):
            oneTableOne.append('X' + '_' + str(i+1) + '_' + str(j+1))
            oneAssignmentFirst.append(oneTableOne)

#Second rule
if range(int(numberOfTables)) > 1:
    for i in range(int(numberOfGuests)):
        for j in range(int(numberOfTables)):
            for k in range(j):
                oneTableTwo = ['~' + 'X' + '_' + str(i+1) + '_' + str(k+1), '~' + 'X' + '_' + str(i+1) + '_' + str(j+1)]
                oneAssignmentSecond.append(oneTableTwo)

del lines[0]

for i in range(len(lines)):
    nextItem = lines[i].replace(' ', '')
    row = nextItem[0]
    col = nextItem[1]
    rel = nextItem[2]

    #a and b cannot sit at any two different tables
    if rel == 'F':
        for i in row:
            for j in col:
                for k in range(int(numberOfTables)):
                    friendListOne = ['~' + 'X' + '_' + str(i) + '_' + str(k+1), 'X' + '_' + str(j) + '_' + str(k+1)]
                    friendListTwo = ['X' + '_' + str(i) + '_' + str(k+1), '~' + 'X' + '_' + str(j) + '_' + str(k+1)]
                    friendList.append(friendListOne)
                    friendList.append(friendListTwo)
    #For each pair of enemies, guest a and guest b
    if rel == 'E':
        for i in row:
            for j in col:
                for k in range(int(numberOfTables)):
                    enemyListOne = ['~' + 'X' + '_' + str(i) + '_' + str(k+1), '~' + 'X' + '_' + str(j) + '_' + str(k+1)]
                    enemyList.append(enemyListOne)

clauses = oneAssignmentFirst + oneAssignmentSecond + friendList + enemyList

def negation(a):
    if('~' in a):
        return a.replace('~', '')
    #return '~' + a;

def check_if_negation_exists(elem):
    if('~' in elem):
        return True

def pl_true(clause, model):
    #print('calling pl_true for clause: ', clause, ' with model: ', model)
    k = list(model.keys())
    result = False
    for literal in clause:
        variable = literal.replace('~','')
        if variable not in k:
            #print('variable ', variable, ' not in model yet')
            return None
        else:
            r = model.get(variable)
            if check_if_negation_exists(literal):
                #print('negation exists:',literal)
                r = (not r)
            result = r or result
    #print('result for clause: ', clause, ' : ', result)
    return result

def dpll(clauses, symbols, _model):
    #print _model
    unknown_clauses = [] ## clauses with an unknown truth value
    for c in clauses:
        val = pl_true(c, _model)
        #print(val)
        if val == False:
            return False
        if val == None:
            unknown_clauses.append(c)
    if not unknown_clauses:
           if len(unknown_clauses) == 0:
                return _model

    if len(symbols) == 0:
        return _model

    symCopy = copy.deepcopy(symbols)
    P = symCopy.pop()
    newVariables = symCopy[:]

    modelNewTrue = copy.deepcopy(_model)
    modelNewFalse = copy.deepcopy(_model)

    modelNewTrue[P] = True
    modelNewFalse[P] = False

    return (dpll(clauses, newVariables, modelNewTrue) or
            dpll(clauses, newVariables, modelNewFalse))

final = dpll(clauses, symbols, {})

f = open('output.txt', 'w')
if bool(final) == False:
    result = 'no'
    f.write(result);
    f.close()
else:
    result = 'yes'
    print result
    f.write(result + '\n')
    for key, value in sorted(final.items()): # returns the dictionary as a list of value pairs -- a tuple.
        if value == True:
            guests = key.split('_')[1]
            tables = key.split('_')[2]
            print guests, tables
            f.write(guests + ' ' + tables + '\n')