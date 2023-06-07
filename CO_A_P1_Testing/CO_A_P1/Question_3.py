import sys

def DecimalToBinary(num):
    binary="{0:b}".format(int(num))
    x=16-len(binary)
    binary='0'*x+binary
    return binary

def BinaryToDecimal(binary):
    i=len(binary)-1
    num=0
    for x in binary:
        num=num+int(x)*pow(2,i)
        i-=1
    return num

def overflowflag(num):
    global registers
    global isFlagNotSet
    if abs(num) >= 10 ** 16:
        registers["111"] = "0" * 12 + "1000"
        isFlagNotSet = False
        num = 0.0
    return num

registers={
    "000":0.0,
    "001":0.0,
    "010":0.0,
    "011":0.0,
    "100":0.0,
    "101":0.0,
    "110":0.0,
    "111":"0"*16
}

memLines={}
for i in range(128):
    memLines[i]="0"*16

lines=[]
memIndex=0

while True:
    try:
        line = input().strip()

        if line == "":
            break

        memLines[memIndex] = line
        memIndex += 1
        lines.append(line)
    except EOFError:
        break

isFlagNotSet=True
isJump=False
isHalt=False

prgCnt=0
prgCntUpd=0

while(prgCnt<len(lines)):
    line=lines[prgCnt]
    opcode=line[:5]
    #typeA Register
    if opcode in ["00000","00001","00110","01010","01011","01100"]:
        reg1=line[7:10]
        reg2=line[10:13]
        reg3=line[13:]
        #addition
        if opcode == "00000":
            registers[reg1]=overflowflag(registers[reg2]+registers[reg3])
        #subtraction
        elif opcode == "00001":
            val=registers[reg2]-registers[reg3]
            if val>=0:
                registers[reg1]=val
            else:
                registers["111"]="0"*12+"1000"
                registers[reg1]=0
                isFlagNotSet=False
        #multiplication
        elif opcode =="00110":
            registers[reg1]=overflowflag(registers[reg2]*registers[reg3])
        #XOR operation
        elif opcode =="01010":
            registers[reg1]=registers[reg2]^registers[reg3]
        #OR_operation
        elif opcode =="01011":
            registers[reg1]=registers[reg2]|registers[reg3]
        #AND_operation
        elif opcode =="01100":
            registers[reg1]=registers[reg2]&registers[reg3]

    #type B Regs
    elif opcode in ["00010","01000","01001"]:
        reg1=line[6:9]
        imm=BinaryToDecimal(line[9:])
        
        #move immediate
        if opcode == "00010":
            registers[reg1]=imm
        #right shift operation
        elif opcode == "01000":
            val=registers[reg1]>>imm
            if val<0:
                registers[reg1]=0
            else:
                registers[reg1]=val
        #left shift operation
        elif opcode == "01001":
            lval=registers[reg1]<<imm
            if (lval>=65536):
                registers[reg1]=0
            else:
                registers[reg1]=lval

    #type C Registers
    elif opcode in ["00011","00111","01101","01110"]:
        reg1=line[10:13]
        reg2=line[13:]
        #move register
        if opcode == "00011":
            registers[reg1]=registers[reg2]
        #divide 
        elif opcode == "00111":
            if registers[reg2] == 0:
                registers["000"]=0
                registers["001"]=0
                isFlagNotSet=False
                registers["111"]="0"*12+"1000"
            else:
                registers["000"]=registers[reg1]//registers[reg2]
                registers["001"]=registers[reg1]%registers[reg2]
        #Invert NOT operations
        elif opcode == "01101":
            lval=DecimalToBinary(registers[reg2])
            s=''
            for bit in lval:
                if bit=='0':
                    s=s+'1'
                else:
                    s=s+'0'
            registers[reg1]=BinaryToDecimal(s)
        #compare
        elif opcode == "01110":
            isFlagNotSet=False
            val= int(registers[reg1])-int(registers[reg2])
            if val >0:
                registers["111"]="0"*12+"0010"
            elif val == 0:
                registers["111"]="0"*12+"0001"
            elif val <0 :
                registers["111"]="0"*12+"0100"

    #type D Registers
    elif opcode in ["00100","00101"]:
        reg1=line[6:9]
        memAddrs=BinaryToDecimal(line[9:])
        #load
        if opcode == "00100":
            registers[reg1]=BinaryToDecimal(memLines[memAddrs])
        #store
        elif opcode == "00101":
            memLines[memAddrs]=DecimalToBinary(registers[reg1])
    #type E Registers
    elif opcode in ["01111","11100","11101","11111"]:
        memAddrs=BinaryToDecimal(line[9:])
        #unconditional jump
        if opcode == "01111":
            prgCntUpd=memAddrs
            isJump=True
        #jump if less than
        elif opcode == "11100":
            if registers["111"]=="0"*12+"0100":
                prgCntUpd=memAddrs
                isJump=True
        #jump if Greater Than
        elif opcode =="11101":
            if registers["111"]=="0"*12+"0010":
                prgCntUpd=memAddrs
                isJump=True
        #jump if Equal
        elif opcode == "11111":
            if registers["111"]=="0"*12+"0001":
                prgCntUpd=memAddrs
                isJump=True
    #type F Regs halt
    elif opcode in ["11010"]:
        isHalt=True

    elif opcode == "10000":
        reg1 = line[7:10]
        reg2 = line[10:13]
        reg3 = line[13:]
        registers[reg1] = registers[reg2] + registers[reg3]
        registers[reg1] = overflowflag(registers[reg1])

    elif opcode == "10001":
        reg1 = line[7:10]
        reg2 = line[10:13]
        reg3 = line[13:]
        registers[reg1] = registers[reg2] - registers[reg3]
        if registers[reg1] < 0:
            registers["111"] = "0" * 12 + "1000"
            registers[reg1] = 0

    elif opcode == "10010":
        reg1 = line[6:9]
        imm = BinaryToDecimal(line[9:])
        registers[reg1] = imm

    if isFlagNotSet==True:
        registers['111']='0'*16

    print(DecimalToBinary(prgCnt)[9:],end='        ')
    print(DecimalToBinary(registers["000"]),end=' ')
    print(DecimalToBinary(registers["001"]),end=' ')
    print(DecimalToBinary(registers["010"]),end=' ')
    print(DecimalToBinary(registers["011"]),end=' ')
    print(DecimalToBinary(registers["100"]),end=' ')
    print(DecimalToBinary(registers["101"]),end=' ')
    print(DecimalToBinary(registers["110"]),end=' ')
    print(registers["111"])

    prgCnt+=1

    if isFlagNotSet==False:  # reset back with 0
        registers['111']='0'*16

    isFlagNotSet=True

    if isJump==True:
        prgCnt=prgCntUpd
        isJump=False
    if isHalt==True:
        break

for memAddrs in memLines:
    print(memLines[memAddrs])
