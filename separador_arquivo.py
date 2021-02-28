# Abrir arquivos dos programas a serem executados
file_code1 = open('codigo1.txt', 'r')
file_code2 = open('codigo2.txt', 'r')

# Arquivos auxiliares
file_funcoes1 = open('funcoes1.txt', 'w')
file_funcoes2 = open('funcoes2.txt', 'w')

file_variaveis1 = open('variaveis1.txt', 'w')
file_variaveis2 = open('variaveis2.txt', 'w')

file_conteudo1 = open('conteudo1.txt', 'w')
file_conteudo2 = open('conteudo2.txt', 'w')

# CODIGO 1 ========================================
# Variaveis auxiliares
aux_funcoes = 0
aux_variaveis = 0
aux_conteudo = 0
# Separação do arquivo 1
for line in file_code1:
    # escrevo as funções no arquivo
    if line != "void main(void) {\n" and aux_funcoes == 0: file_funcoes1.writelines(line)
    elif line == "void main(void) {\n": aux_funcoes = 1
    
    # escrevo as funcoes
    if aux_funcoes == 1 and aux_variaveis == 0:
        if line == "void main(void) {\n": aux_variaveis = 0
        elif 'int' in line: file_variaveis1.writelines(line)
        else: aux_variaveis = 1
    # escrevo o conteudo
    if aux_variaveis == 1:
        file_conteudo1.writelines(line)

file_funcoes1.close()
file_variaveis1.close()
file_conteudo1.close()

# CODIGO 2 ========================================
# Variaveis auxiliares
aux_funcoes = 0
aux_variaveis = 0
aux_conteudo = 0
# Separação do arquivo 1
for line in file_code2:
    # escrevo as funções no arquivo
    if line != "void main(void) {\n" and aux_funcoes == 0: file_funcoes2.writelines(line)
    elif line == "void main(void) {\n": aux_funcoes = 1
    
    # escrevo as funcoes
    if aux_funcoes == 1 and aux_variaveis == 0:
        if line == "void main(void) {\n": aux_variaveis = 0
        elif 'int' in line: file_variaveis2.writelines(line)
        else: aux_variaveis = 1
    # escrevo o conteudo
    if aux_variaveis == 1:
        file_conteudo2.writelines(line)

file_funcoes2.close()
file_variaveis2.close()
file_conteudo2.close()

