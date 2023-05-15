


def DecimalToBinary(num):
    bine="{0:b}".format(int(num))
    x=7-len(bine)
    bine='0'*x+bine
    return bine

def register_check(reg,i):
    if reg not in registers.keys():
        file_output.write("Error, Use of Invalid register in line"+str(i))
        exit()
    
def all_variable_definition_at_begining(stmts):
    for i in range(len(stmts)):
        count=0
        if stmts[i][0]:
            if count==1:
                file_output.write("Error, All the variable definition are not made at the begining og the assembly language, speciically "+stmts[i][0]+" in line "+str(i))
                exit()
        else:
            count=1

def immediate_check(imm, i):
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
def typeA_checker(stmt, i):
    if len(stmt) !=4:
        file_output.write("Error, invalid Number of Arguments for Type-A Instruction in line "+str([i]))
        exit()
    register_check(stmt[1],i)
    register_check(stmt[2],i)
    register_check(stmt[3],i)
def typeB_checker(stmt,i):
    if len(stmt) !=3:
        file_output.write("Error, Invalid Number of arguments for Type-B instruction in line ")+str([i])
        exit()
    register_check(stmt[1],i)
    register_check(stmt[2],i)
def typeC_checker(stmt,i):
    if len(stmt) !=3:
        file_output.write("Error, Invalid Number of arguments for Type-B instruction in line ")+str([i])
        exit()
    register_check(stmt[1],i)
    register_check(stmt[2],i)
def typeD_checker(stmt, i):
    if len(stmt) !=3:
        file_output.write("Error, Invalid Number of Arguments for Type-D Instruction in line "+stmt([i]))
        exit()
def typeE_checker(stmt, i):
    if len(stmt) !=2:
        file_output.write("Error, Invalid Number of Argument for type-E Instruction in line "+str([i]))
        exit()
def typeF_checker(stmt, i):
    if len(stmt) !=1:
        file_output.write("Error, Invalid Number of Arguments for Type-F Instriuction in line "+str([i]))
        exit()
        
import sys

file_input=sys.stdin
file_output=sys.stdout

print("Etawah Supremacy")