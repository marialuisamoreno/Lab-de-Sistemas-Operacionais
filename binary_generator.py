def binary(numero):
    #converto para binário
    aux = f'{int(numero):09b}'
    aux = str(aux)
    #removo os caracteres 0b
    aux = aux[2 : ]
    tamanho = len(aux)
    #completo com zeros faltantes
    zeros = ''
    for i in range(9-tamanho):
        zeros += "0"
    return zeros + aux

def Instrucao(opcode, RC, RB, RA):
    RC = str(RC)
    RB = str(RB)
    RA = str(RA)

    if opcode == 'jp':
        memoria1 = "10010"
        memoria2 = binary(RC)
        memoria3 = binary(0)
        memoria4 = binary(0)

    elif opcode == 'ld':
        memoria1 = "10001"
        memoria2 = binary(RC)
        memoria3 = binary(RB)
        memoria4 = binary(0)

    elif opcode == 'rd':
        memoria1 = "10110"
        memoria2 = binary(RC)
        memoria3 = binary(0)
        memoria4 = binary(0)

    elif opcode == 'pt':
        memoria1 = "10111"
        memoria2 = binary(RC)
        memoria3 = binary(0)
        memoria4 = binary(0)

    elif opcode == 'st':
        memoria1 = "00110"
        memoria2 = binary(RC)
        memoria3 = binary(RB)
        memoria4 = binary(0)

    elif opcode == 'li':
        memoria1 = "00101"
        memoria2 = binary(RC)
        memoria3 = binary(RB)
        memoria4 = binary(0)

    elif opcode == 'beq':
        memoria1 = "10101"
        memoria2 = binary(RC)
        memoria3 = binary(RB)
        memoria4 = binary(RA)

    elif opcode == 'sum':
        memoria1 = "00000"
        memoria2 = binary(RC)
        memoria3 = binary(RB)
        memoria4 = binary(RA)

    elif opcode == 'sub':
        memoria1 = "00001"
        memoria2 = binary(RC)
        memoria3 = binary(RB)
        memoria4 = binary(RA)

    elif opcode == 'mt':
        memoria1 = "00010"
        memoria2 = binary(RC)
        memoria3 = binary(RB)
        memoria4 = binary(RA)

    elif opcode == 'div':
        memoria1 = "00011"
        memoria2 = binary(RC)
        memoria3 = binary(RB)
        memoria4 = binary(RA)

    elif opcode == 'slt':
        memoria1 = "01111"
        memoria2 = binary(RC)
        memoria3 = binary(RB)
        memoria4 = binary(RA)

    elif opcode == 'eq':
        memoria1 = "01101"
        memoria2 = binary(RC)
        memoria3 = binary(RB)
        memoria4 = binary(RA)

    elif opcode == 'sgt':
        memoria1 = "01110"
        memoria2 = binary(RC)
        memoria3 = binary(RB)
        memoria4 = binary(RA)
    
    else:
        memoria1 = "10000"
        memoria2 = binary(RC)
        memoria3 = binary(RB)
        memoria4 = binary(RA)

    return memoria1 + memoria2 + memoria3 + memoria4

# Abrir arquivo do Código Assembly
file_assembly = open('assembly_operationalSys.txt', 'r')
labels = {}
linha = 0
cont_instrucao = 0;

# Ler o local dos labels
for line in file_assembly:
    instrucao = line.split(" ")

    # labels
    if len(instrucao) == 1:
        instrucao[0] = instrucao[0].replace('\n', '')
        if instrucao[0] not in labels.keys(): 
            labels[instrucao[0]] = linha
    linha += 1

file_assembly.close()
file_assembly = open('assembly_operationalSys.txt', 'r')
file_binary = open('binary_operationalSys.txt', 'w')

for line in file_assembly:
    expressao = ''
    instrucao = line.split(" ")

    #labels
    if len(instrucao) == 1:
        instrucao[0] = instrucao[0].replace('\n', '')
        expressao = Instrucao('nop', 0, 0, 0)

    # Input, Output, Jump
    if len(instrucao) == 2:
        instrucao[1] = instrucao[1].replace('\n', '')
        
        if instrucao[1][0] == '$':
            instrucao[1] = instrucao[1].replace('$', '')
            instrucao[1] = instrucao[1].replace('r', '')
            instrucao[1] = instrucao[1].replace('m', '')
            rc = instrucao[1]

            expressao = Instrucao(instrucao[0], rc, 0, 0)
        else:
            rc = labels[instrucao[1]]
            expressao = Instrucao(instrucao[0], rc, 0, 0)
    
    # Load, Load Imediate, Store
    if len(instrucao) == 3:
        instrucao[2] = instrucao[2].replace('\n', '')

        instrucao[1] = instrucao[1].replace('$', '')
        instrucao[1] = instrucao[1].replace('r', '')
        rc = instrucao[1]
        instrucao[2] = instrucao[2].replace('$', '')
        instrucao[2] = instrucao[2].replace('m', '')
        rb = instrucao[2]

        expressao = Instrucao(instrucao[0], rc, rb, 0)
    
    # Operações lógicas/Aritméticas
    if len(instrucao) == 4:
        instrucao[3] = instrucao[3].replace('\n', '')

        if instrucao[0] == 'beq':
            if instrucao[1] == 'linha_atual+2':
                rc = linha + 2
            else: rc = labels[instrucao[1]]
        else:
            instrucao[1] = instrucao[1].replace('$', '')
            instrucao[1] = instrucao[1].replace('r', '')
            rc = instrucao[1]
        instrucao[2] = instrucao[2].replace('$', '')
        instrucao[2] = instrucao[2].replace('r', '')
        rb = instrucao[2]
        instrucao[3] = instrucao[3].replace('$', '')
        instrucao[3] = instrucao[3].replace('r', '')
        ra = instrucao[3]

        expressao = Instrucao(instrucao[0], rc, rb, ra)

    linha += 1

    #file_binary.writelines(expressao + " /* " + instrucao[0] + " */\n")
    file_binary.writelines("RAM[" + str(cont_instrucao) + "] = 32'b" + expressao + ";\n")
    cont_instrucao += 1

file_assembly.close()
file_binary.close()