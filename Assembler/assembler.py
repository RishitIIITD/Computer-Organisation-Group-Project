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
        file_output.write("Error, Use of Invalid register in line"+str(i))
        exit()
    
def variable_begin_at_start(statements):
    for i in range(len(statements)):
        count=0
        if statements[i][0]:
            if count==1:
                file_output.write("Error, All the variable definition are not made at the begining og the assembly language, speciically "(statements[i][0]+" in line "+str(i)))
                exit()
        else:
            count=1

def imm_check(imm, i):
    if "$"!=imm[0]:
        file_output.write("Error, Immediate not probided, line "+str(i))
        exit()
    try:
        x=int(imm[1:])
        if(x>=128 or x<0):
            file_output.write("Error,, The Immdiate exceeds the limit from 0 to 127, line  "+str(i))
            exit()
    except ValueError:
        file_output.write("Error, The immediate should be a whole number, line "+str(i))
        exit()
def typeA_checker(statements, i):
    if len(statements) != 4:
        file_output.write("Error, invalid Number of Arguments for Type-A Instruction in line "+str([i]))
        exit()
    register_check(statements[1],i)
    register_check(statements[2],i)
    register_check(statements[3],i)

def typeB_checker(statements,i):
    if len(statements) != 3:
        file_output.write("Error, Invalid Number of arguments for Type-B instruction in line ")+str([i])
        exit()
    register_check(statements[1],i)
    imm_check(statements[2],i)

def typeC_checker(statements,i):
    if len(statements) != 3:
        file_output.write("Error, Invalid Number of arguments for Type-B instruction in line ")+str([i])
        exit()
    register_check(statements[1],i)
    register_check(statements[2],i)

def typeD_checker(statements, i):
    if len(statements) != 3:
        file_output.write("Error, Invalid Number of Arguments for Type-D Instruction in line "+statements([i]))
        exit()

def typeE_checker(statements, i):
    if len(statements) != 2:
        file_output.write("Error, Invalid Number of Argument for type-E Instruction in line "+str([i]))
        exit()

def typeF_checker(statements, i):
    if len(statements) != 1:
        file_output.write("Error, Invalid Number of Arguments for Type-F Instriuction in line "+str([i]))
        exit()
