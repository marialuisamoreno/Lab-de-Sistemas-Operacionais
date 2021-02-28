# Controle de Memória
BancoRegistradores = {}
BancoMemoria = {}
funcoes = {}
registrador = 0
memoria = 0
last_func = ""

def BancoReg (dado):
    global registrador
    if dado in BancoRegistradores.keys(): 
        return BancoRegistradores[dado]
    else: 
        BancoRegistradores[dado] = "$r" + str(registrador)
        registrador+=1
        return BancoRegistradores[dado]

def BancoMem (dado):
    global memoria
    if dado in BancoMemoria.keys(): 
        return BancoMemoria[dado]
    else: 
        BancoMemoria[dado] = "$m" + str(memoria)
        memoria+=1
        return BancoMemoria[dado]

def EmpilhaParametros (funcao, men):
    if funcao in funcoes.keys(): 
        funcoes[funcao].append(men)
    else:
        funcoes[funcao] = []
        funcoes[funcao].append(men)

def DesempilhaParamentros (funcao, pos):
    if funcao == "parametros":
        return funcoes[funcao].pop()
    else:
        return funcoes[funcao][pos]

# Abrir arquivo do Código Intermediário
file_intermediario = open('saida_operationalSys.txt', 'r')

# Abrir arquivo auxiliar
file_assembly = open('assembly_operationalSys.txt', 'w')

# Transformar o código intermediário em código assembly
check = 0
for line in file_intermediario:
    # Ler a partir de onde o código está
    if line == "Intermediate Code:\n": 
        check = 1
        file_assembly.writelines("jp main\n")
    
    if check:
        parametros = line.split(", ")
        if len(parametros) > 2:
            parametros[3] = parametros[3].replace("\n", "")
        
        # Declaração de Função
        if parametros[0] == "FUNC": 
            if last_func != "":
                file_assembly.writelines("jp chamada_" + last_func + "\n")

            nome_funcao = parametros[2]
            last_func = parametros[2]
            file_assembly.writelines(nome_funcao + "\n")
            if parametros[1] == "INT":
                men = BancoMem(parametros[2])

        # Carregar dados numa função
        if parametros[0] == "LOAD":
            reg = BancoReg(parametros[1])
            men = BancoMem(parametros[1])
            EmpilhaParametros(last_func, men)
            file_assembly.writelines("ld " + reg + " " + men + "\n")
        
        # Parâmetro de função
        if parametros[0] == "PARAM":
            reg = BancoReg(parametros[1])
            men = BancoMem(parametros[1])
            file_assembly.writelines("ld " + reg + " " + men + "\n")
            EmpilhaParametros("parametros", reg)
        
        # Chamada de função
        if parametros[0] == "CALL":
            if (parametros[1] == "input"):
                entrada = BancoMem("input")
                file_assembly.writelines("rd " + entrada + "\n")

            elif (parametros[1] == "output"):
                last_reg = DesempilhaParamentros("parametros", 0)
                file_assembly.writelines("pt " + last_reg + "\n")

            else:
                qtd_parametros = int(parametros[2])
                for i in range(qtd_parametros):
                    reg = DesempilhaParamentros("parametros", 0)
                    men = DesempilhaParamentros(parametros[1], qtd_parametros-i-1)
                    file_assembly.writelines("st " + reg + " " + men + "\n")

                file_assembly.writelines("jp " + parametros[1] + "\n")
                file_assembly.writelines("chamada_" + parametros[1] + "\n")

        # Salvar endereço
        if parametros[0] == "ASSIGN":
            reg = BancoReg(parametros[1])
            if parametros[2].isdigit():
                men = parametros[2]
                file_assembly.writelines("li " + reg + " " + parametros[2] + "\n")
            else:
                men = BancoMem(parametros[2])
                file_assembly.writelines("ld " + reg + " " + men + "\n")
            men = BancoMem(parametros[1])
            file_assembly.writelines("st " + reg + " " + men + "\n")
        
        # Declaração do label
        if parametros[0] == "LABEL":
            file_assembly.writelines(parametros[1] + "\n")
        
        # Pular para o label
        if parametros[0] == "JUMP":
            file_assembly.writelines("jp " + parametros[1] + "\n")

        # "se não", pular para o label
        if parametros[0] == "IF_NOT":
            reg1 = BancoReg(parametros[1])
            reg2 = BancoReg("falso")
            endereco = parametros[2]
            file_assembly.writelines("li " + reg2 + " 0" + "\n")
            file_assembly.writelines("beq " + endereco + " " + reg1 + " " + reg2 + "\n")

        # Retorno de uma função
        if parametros[0] == "JR":
            reg = BancoReg(last_func)
            men = BancoMem(parametros[1])
            file_assembly.writelines("ld " + reg + " " + men + "\n")
        
        # Operação de soma
        if parametros[0] == "ADD":
            vetor = parametros[1]
            # Caso esteja tentando atribuir um valor para um determinada posição do vetor
            if vetor[0] == "V" and vetor[1] == "E" and vetor[2] == "T":
                men_pos_inical = BancoMem(parametros[2])
                reg_pos_inical = BancoReg(parametros[2])
                file_assembly.writelines("ld " + reg_pos_inical + " " + men_pos_inical + "\n")
                
                # Se for dígito, já tenho o incremento
                if parametros[3].isdigit():
                    reg_incremento = BancoReg("aux_incremento")
                    file_assembly.writelines("li " + reg_incremento + " " + parametros[3] + "\n")
                    posicao = BancoReg("aux_posicao")
                    file_assembly.writelines("sum " + posicao + " " + reg_pos_inical + " " + reg_incremento + "\n")
                    posicaoM = BancoMem(posicao)
                    file_assembly.writelines("st " + posicao + " " + posicaoM + "\n")
                    reg = BancoReg(parametros[1])
                    file_assembly.writelines("ld " + reg + " " + posicaoM + "\n")
                    men = BancoMem(parametros[1])
                    file_assembly.writelines("st " + reg + " " + men + "\n")
                
                # Encontrar o incremento
                else:
                    incremento = BancoMem(parametros[3])
                    reg_incremento = BancoReg("aux_incremento")
                    file_assembly.writelines("ld " + reg_incremento + " " + incremento + "\n")
                    posicao = BancoReg("aux_posicao")
                    file_assembly.writelines("sum " + posicao + " " + reg_pos_inical + " " + reg_incremento + "\n")
                    posicaoM = BancoMem(posicao)
                    file_assembly.writelines("st " + posicao + " " + posicaoM + "\n")
                    reg = BancoReg(parametros[1])
                    file_assembly.writelines("ld " + reg + " " + posicaoM + "\n")
                    men = BancoMem(parametros[1])
                    file_assembly.writelines("st " + reg + " " + men + "\n")

            # operação de soma
            else:
                reg1 = BancoReg(parametros[1])
                # Se for dígito, salvar num reg intermediário
                if parametros[2].isdigit():
                    reg2 = BancoReg("aux_soma1")
                    file_assembly.writelines("li " + reg2 + " " + parametros[2] + "\n")
                else: reg2 = BancoReg(parametros[2])

                # Se for dígito, salvar num reg intermediário
                if parametros[3].isdigit():
                    reg3 = BancoReg("aux_soma2")
                    file_assembly.writelines("li " + reg3 + " " + parametros[3] + "\n")
                else: reg3 = BancoReg(parametros[3])
                
                file_assembly.writelines("sum " + reg1 + " " + reg2 + " " + reg3 + "\n")

                men = BancoMem(parametros[1])
                file_assembly.writelines("st " + reg1 + " " + men + "\n")

        # Operação de subtração 
        if parametros[0] == "SUB":
            reg1 = BancoReg(parametros[1])
            if parametros[2].isdigit(): reg2 = parametros[2]
            else: reg2 = BancoReg(parametros[2])
            if parametros[3].isdigit(): reg3 = parametros[3]
            else: reg3 = BancoReg(parametros[3])
            
            file_assembly.writelines("sub " + reg1 + " " + reg2 + " " + reg3 + "\n")

            men = BancoMem(parametros[1])
            file_assembly.writelines("st " + reg1 + " " + men + "\n")
        
        # Operação de multiplicação
        if parametros[0] == "MULT":
            reg1 = BancoReg(parametros[1])
            if parametros[2].isdigit(): reg2 = parametros[2]
            else: reg2 = BancoReg(parametros[2])
            if parametros[3].isdigit(): reg3 = parametros[3]
            else: reg3 = BancoReg(parametros[3])
            
            file_assembly.writelines("mt " + reg1 + " " + reg2 + " " + reg3 + "\n")

            men = BancoMem(parametros[1])
            file_assembly.writelines("st " + reg1 + " " + men + "\n")
        
        # Operação de divisão
        if parametros[0] == "DIV":
            reg1 = BancoReg(parametros[1])
            if parametros[2].isdigit(): reg2 = parametros[2]
            else: reg2 = BancoReg(parametros[2])
            if parametros[3].isdigit(): reg3 = parametros[3]
            else: reg3 = BancoReg(parametros[3])
            
            file_assembly.writelines("div " + reg1 + " " + reg2 + " " + reg3 + "\n")

            men = BancoMem(parametros[1])
            file_assembly.writelines("st " + reg1 + " " + men + "\n")
        
        # Operação de menor
        if parametros[0] == "SLT":
            reg1 = BancoReg(parametros[1])
            if parametros[2].isdigit(): reg2 = parametros[2]
            else: reg2 = BancoReg(parametros[2])
            if parametros[3].isdigit(): reg3 = parametros[3]
            else: reg3 = BancoReg(parametros[3])
            
            file_assembly.writelines("slt " + reg1 + " " + reg2 + " " + reg3 + "\n")
        
        # Operação de menor igual
        if parametros[0] == "SLTE":
            reg1 = BancoReg(parametros[1])
            if parametros[2].isdigit(): reg2 = parametros[2]
            else: reg2 = BancoReg(parametros[2])
            if parametros[3].isdigit(): reg3 = parametros[3]
            else: reg3 = BancoReg(parametros[3])
            
            file_assembly.writelines("slt " + reg1 + " " + reg2 + " " + reg3 + "\n")

            reg4 = BancoReg("verdadeiro")
            file_assembly.writelines("li " + reg4 + " 1" + "\n")
            file_assembly.writelines("beq " + "linha_atual+2" + " " + reg1 +" " + reg4 + "\n")
            file_assembly.writelines("eq " + reg1 + " " + reg2 + " " + reg3 + "\n")
        
        # Operação de maior
        if parametros[0] == "SGT":
            reg1 = BancoReg(parametros[1])
            if parametros[2].isdigit(): reg2 = parametros[2]
            else: reg2 = BancoReg(parametros[2])
            if parametros[3].isdigit(): reg3 = parametros[3]
            else: reg3 = BancoReg(parametros[3])
            
            file_assembly.writelines("sgt " + reg1 + " " + reg2 + " " + reg3 + "\n")
        
        # Operação de maior igual
        if parametros[0] == "SGTE":
            reg1 = BancoReg(parametros[1])
            if parametros[2].isdigit(): reg2 = parametros[2]
            else: reg2 = BancoReg(parametros[2])
            if parametros[3].isdigit(): reg3 = parametros[3]
            else: reg3 = BancoReg(parametros[3])
            
            file_assembly.writelines("sgt " + reg1 + " " + reg2 + " " + reg3 + "\n")

            reg4 = BancoReg("verdadeiro")
            file_assembly.writelines("li " + reg4 + " 1" + "\n")
            file_assembly.writelines("beq " + "linha_atual+2" + " " + reg1 + reg4 + "\n")
            file_assembly.writelines("eq " + reg1 + " " + reg2 + " " + reg3 + "\n")
        
        # Operação de igualdade
        if parametros[0] == "EQUAL":
            reg1 = BancoReg(parametros[1])
            if parametros[2].isdigit(): reg2 = parametros[2]
            else: reg2 = BancoReg(parametros[2])
            if parametros[3].isdigit(): reg3 = parametros[3]
            else: reg3 = BancoReg(parametros[3])
            
            file_assembly.writelines("eq " + reg1 + " " + reg2 + " " + reg3 + "\n")
        
        # Alocação de memória
        if parametros[0] == "ALOC_MEN":
            qtd = int(parametros[2])
            if qtd == 1:
                men = BancoMem(parametros[1])
                
            else:
                men = BancoMem(parametros[1])
                for i in range(int(parametros[2])):
                    men = BancoMem(parametros[1] + "_" + str(i))

file_intermediario.close()
file_assembly.close()