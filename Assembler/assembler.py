import sys

file_input=sys.stdin
file_output=sys.stdout

opcodes={
   "add":"00000",
   "sub":"00001",
   "mov":"00010",
   "movr":"00011",
   "ld":"00100",
   "st":"00101",
   "mul":"00110",
   "div":"00111",
   "rs":"01000",
   "ls":"01001",
   "xor":"01010",
   "or":"01011",
   "and":"01100",
   "not":"01101",
   "cmp":"01110",
   "jmp":"01111",
   "jlt":"11100",
   "jgt":"11101",
   "je":"11111",
   "hlt":"11010",
}

registers={
    "R0":"000",
    "R1":"001",
    "R2":"010",
    "R3":"011",
    "R4":"100",
    "R5":"101",
    "R6":"110",
    "FLAGS":"111",
}

def DecimalToBinary(num):
    bine="{0:b}".format(int(num))
    x=7-len(bin)
    bine='0'*x+bin
    return bin

def register_check(reg,i):
    if reg not in registers.keys():
        file_output.write("Error, Use of Invalid register in line: "+str(i))
        exit()
    
def variable_begin_at_start(statements):
    for i in range(len(statements)):
        count=0
        if statements[i][0]:
            if count==1:
                file_output.write("Error, All the variable definition are not made at the begining og the assembly language, speciically "(statements[i][0]+" in line: "+str(i)))
                exit()
        else:
            count=1

def imm_check(imm, i):
    if "$"!=imm[0]:
        file_output.write("Error, Immediate not probided, line: "+str(i))
        exit()
    try:
        x=int(imm[1:])
        if(x>=128 or x<0):
            file_output.write("Error,, The Immdiate exceeds the limit from 0 to 127, line: "+str(i))
            exit()
    except ValueError:
        file_output.write("Error, The immediate should be a whole number, line: "+str(i))
        exit()
def typeA_checker(statements, i):
    if len(statements) != 4:
        file_output.write("Error, invalid Number of Arguments for Type-A Instruction in line: "+str([i]))
        exit()
    register_check(statements[1],i)
    register_check(statements[2],i)
    register_check(statements[3],i)

def typeB_checker(statements,i):
    if len(statements) != 3:
        file_output.write("Error, Invalid Number of arguments for Type-B instruction in line: ")+str([i])
        exit()
    register_check(statements[1],i)
    imm_check(statements[2],i)

def typeC_checker(statements,i):
    if len(statements) != 3:
        file_output.write("Error, Invalid Number of arguments for Type-B instruction in line: ")+str([i])
        exit()
    register_check(statements[1],i)
    register_check(statements[2],i)

def typeD_checker(statements, i):
    if len(statements) != 3:
        file_output.write("Error, Invalid Number of Arguments for Type-D Instruction in line: "+statements([i]))
        exit()

def typeE_checker(statements, i):
    if len(statements) != 2:
        file_output.write("Error, Invalid Number of Argument for type-E Instruction in line: "+str([i]))
        exit()

def typeF_checker(statements, i):
    if len(statements) != 1:
        file_output.write("Error, Invalid Number of Arguments for Type-F Instriuction in line: "+str([i]))
        exit()

statements=[]
for line in file_input:
    line=line.strip()
    if line=="\n" or line==" " or line=="":
        continue
    lst=line.split()
    statements.append(lst)
    if line=="q":
        file_output.write("You entered q\n")
    if line=="hlt":
        break

print(len(statements))

for i in statements:
    print(i)

for i in range(len(statements)):
    if statements[i][0] in ["mov","ls","rs"]:
        try:
            if ('$' not in statements[i][2]):
                statements[i][0]=statements[i][0]+'r'
        except:
            file_output.write("Error, Immediate not in line: "+str(i))
            exit()

labels={}
program_counter=0
for i in range(len(statements)):
    if statements[i][0][len(statements[i][0]-1)]==':':
        file_output.write("Error, Invalid statement in line: ",+str(i))
        exit()
    labels[statements[i][0][:-1]]=program_counter
    statements.remove(statements[i][0])
    if len(statements[i])==0:
        file_output.write("Error, empty label in line: "+str(i))
        exit()
    if statements[i][0]!="var":
        program_counter+=1

for line in statements:
    if len(line)==0:
        statements.remove(line)

if len(statements)>128:
    file_output.write("Error, No. of instructions more than 128")
    exit()

for i in range(len(statements)):
    if statements[i][0] not in opcodes.keys() and statements[i][0]!="var":
        file_output.write("Error, Invalid instruction name in line: "+str(i))
        exit()

instructions={}
mem_address=0
for i in range(len(statements)):
    if statements[i][0]!="var":
        mem_address+=1

variable_begin_at_start(statements)
vars={}
for i in range(len(statements)):
    if statements[i][0]=="var":
        vars[statements[i][1]]=mem_address
        mem_address+=1

for i in range(len(statements)):
    if statements[i][0] in ["ld","st"]:
        if statements[i][2] not in vars:
            file_output.write("Error, Undefined variable used in line: "+str(i))
            exit()
    if statements[i][0] in ["jmp","jlt","jgt","je"]:
        if statements[i][1] not in labels.keys():
            file_output.write("Error, Undefined label used in line: "+str(i))
            exit()

hlt_present=False
for i in range(len(statements)):
    if "hlt" in statements[i]:
        if i==len(statements)-1:
            if (statements[i][0]=="hlt" and len(statements[i]==1)):
                hlt_present=True
            else:
                file_output.write("Error,  Invalid Use of hlt instruction in line: "+str(i))
                exit()
        else:
            file_output.write("Error, hlt must be the last instruction in line: "+str(i))
            exit()
if not(hlt_present):
    file_output.write("Error, missing hlt instruction")
    exit()

def get_memaddressA(mem_address):
    return vars[mem_address]

def get_memaddress(mem_address):
    return labels[mem_address]

def typeA(mem_address):
    return opcodes[statements[0]] + "0"*2 + registers[statements[1]] + registers[statements[2]] + registers[statements[3]]

def typeB (mem_address):
    return (opcodes[statements[0]] + registers[statements[1]] + DecimalToBinary(int(statements[2])))

def typeC(statements):
    return opcodes[statements[0]] +"0"*5 + registers[statements[1]] + registers[statements[2]]

def typeD(statements):
    return opcodes[statements[0]] + "0" + registers[statements[1]] + DecimalToBinary(int(get_memaddressA(statements[2])))
    
def typeE(statements):
    return (opcodes[statements[0]]+ "0"*4 + DecimalToBinary(int(get_memaddress(statements[1]))))

def typeF(statements):
    return opcodes[statements[0]]+ "0"*11

for i in range(len(statements)):
    if('FLAGS' in statements[i]):
        if(len(statements[i])!=3 or statements[i][0]!='movr' or statements[i][1]!='FLAGS'):
            file_output.write("Error,In use of FLAGS register in line "+str(i))
            exit()
        else:
            typeC_checker(statements[i],i)
    if(statements[i][0] in ['add','sub','mul','xor','or','and']):
        typeA_checker(statements[i], i)

    elif(statements[i][0] in ['mov','ls','rs']):
        typeB_checker(statements[i], i)

    elif(statements[i][0] in ['movr','div','not','cmp']):
        typeC_checker(statements[i], i)

    elif(statements[i][0] in ['ld','st']):
        typeD_checker(statements[i], i)

    elif(statements[i][0] in ['jmp','jlt','jgt','je']):
        typeE_checker(statements[i], i)

    elif(statements[i][0]=="hlt"):
        typeF_checker(statements[i], i)

for i in range(len(statements)):
    if statements[i][0] in ['mov','ls','rs']:
        if("$" in statements[i][2]):
            statements[i][2]=statements[i][2][1:]

for i in range(len(statements)):
    if(statements[i][0] in ['add','sub','mul','xor','or','and']):
        file_output.write(typeA(statements[i])+"\n")

    elif(statements[i][0] in ['mov','ls','rs']):
        file_output.write(typeB(statements[i])+"\n")

    elif(statements[i][0] in ['movr','div','not','cmp']):
        file_output.write(typeC(statements[i])+"\n")

    elif(statements[i][0] in ['ld','st']):
        file_output.write(typeD(statements[i])+"\n")

    elif(statements[i][0] in ['jmp','jlt','jgt','je']):
        file_output.write(typeE(statements[i])+"\n")

    elif(statements[i][0]=="hlt"):
        file_output.write(typeF(statements[i]))

file_output.close()