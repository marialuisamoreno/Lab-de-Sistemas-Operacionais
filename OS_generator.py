def intercala(L,L2):
    intercalada = []
    for a,b in zip(L, L2):
        intercalada.append(a)
        intercalada.append(b)
    return intercalada

# Abrir arquivos dos programas a serem executados
file_code1 = open('conteudo1.txt', 'r')
file_code2 = open('conteudo2.txt', 'r')

processos1 = []
processos2 = []

# PROCESSOS 1 ====================================
temp = ""
aux = 0
pilha1 = []
for line in file_code1:
    if '{' in line:
        temp = temp + line
        pilha1.append('{')
        aux = 1

    if '}' in line: pilha1.pop(0)

    if aux == 1 and '{' not in line: temp = temp + line

    if aux == 0: processos1.append(line)

    if len(pilha1) == 0 and temp != '' and temp not in processos1:
        processos1.append(temp)
        aux = 0

file_code1.close()

# PROCESSOS 2 ====================================
temp = ""
aux = 0
pilha2 = []
for line in file_code2:
    if '{' in line:
        temp = temp + line
        pilha2.append('{')
        aux = 1

    if '}' in line: pilha2.pop(0)

    if aux == 1 and '{' not in line: temp = temp + line

    if aux == 0: processos2.append(line)

    if len(pilha2) == 0 and temp != '' and temp not in processos2:
        processos2.append(temp)
        aux = 0

file_code2.close()

# INTERCALAR PROCESSOS ===========================
file_saida = open('temp_conteudo.txt', 'w')
print("Which file has the highest priority? [1/2] ")
prioridade = input()
if prioridade == '1': listaIntercalada = intercala(processos1, processos2)
else: listaIntercalada = intercala(processos2, processos1)

for i in listaIntercalada:
    file_saida.writelines(i)

file_saida.close()