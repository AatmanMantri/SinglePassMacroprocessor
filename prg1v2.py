import re
import sys
import os


#Command line arguments
if len(sys.argv)!=3:
    print("Usage: 3 parameters - argv[1] input file name, argv[2] output lex file ")    
    sys.exit()

input_file=sys.argv[1]
output_file=sys.argv[2]


NAMTAB = {}
DEFTAB = []
ARGTAB = {}
DEFTAB = []
content = []
realcontent = []


##########Function definitions##########


#Stuff to be written to the lex file
lex_header = '%{\n#include<stdio.h>\n%}\n'
lex_footer = 'int main()\n{\n\tyyin = fopen("testprogmod.asm", "r");\n\tyyout = fopen("testprogresult.asm", "w");\n\tyylex();\n}\nint yywrap()\n{\n\treturn 1;\n}'
lex_rules_delim = '%'+'%\n'
lex_rules = ''
lex_rule = ''


#Writing into the lex file 
def writer(lex_rules):
    with open(output_file,'w') as f:
        lex_rules = lex_rules_delim + lex_rules + lex_rules_delim
        f.write(lex_header)
        f.write(lex_rules)
        f.write(lex_footer)

#List all the arguments for the macro
def defineargs(item):
    ARGTAB[item[0]]=item[2:]
    # print(ARGTAB)

#Replace the function defintion with the called parameters
def replaceargs(replacement,item):
    # print(ARGTAB)
    if(len(item)-1 != len(ARGTAB[item[0]])):
        print("Wrong number of arguments for the call ")
        sys.exit()

    for index,arg in enumerate(item[1:]):
        replacement=replacement.replace(ARGTAB[item[0]][index],arg)
    return replacement

#Adding to NAMTAB and DEFTAB
def defineline(item):
    NAMTAB[item[0]] = len(DEFTAB)
    x = realcontent.index(item)
    abc = ''
    defineargs(item)
    for i in range(x+1, len(content)):   
        if(str(content[i]) == 'endm'):
            DEFTAB.append(abc)
            return
        else:
            abc = abc + str(content[i]) + '\\n'


##########End of function definitions##########

##########Execution##########

# Read contents from file
with open(input_file) as f:
    contentx = f.readlines()

#Preprocessing the content
for item in contentx:
    if ':' in item:
        x = item.split(':')[0].strip() + ':'
        y = '\n' + item.split(':')[1].strip() + '\n'
        content.append(x.lower())
        content.append(y.lower())
    else:
        content.append(item.lower().strip() + '\n')

# Write changes to a file
with open('testprogmod.asm', 'w') as f:
    f.writelines(content)  
    
content = [x.strip() for x in content] 


#Tokenize each line
for item in content:
    item=re.split(' |,',item)
    if '' in item:
        item.remove('')
    realcontent.append(item)
print(realcontent)
#print(content)
#print(realcontent)

#The main 1 pass code. 
for item in realcontent:
    # First check if there's a macro defintion
    if len(item) >= 2:
        if item[1] == 'macro':
            # print(item[0])
            defineline(item)
            continue
    #Check for the macro calls
    for word in item:
        if word in NAMTAB:
            index = int(NAMTAB[word])
            replacement = DEFTAB[index]
            index=item.index(word)
            replacement=replaceargs(replacement,item)
            print(replacement)
            lex_rule = '"'+' '.join(item)+'"'
            lex_rule += ' { fprintf(yyout, "\\n'+replacement+'");}\n'
            lex_rules += lex_rule
            lex_rule = ''
            break

writer(lex_rules)

# For execution of the lexer - uses UNIX commands
os.system('lex ' + sys.argv[2] + ' && cc -Wall -std=c99 lex.yy.c -o lexy.o && ./lexy.o')

# For cleanup of unnecessary files - Can be modified as required - Uses UNIX commands
os.system('rm -f testprogmod.asm lex.yy.c lexy.o '+sys.argv[2])
