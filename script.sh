# Script para a compilação de código em C-
# Desenvolvido por Maria Luisa Santos Moreno Sanches
# e por André Lucas Maegina na disciplina de Compiladores
# do ICT_UNIFESP 2019

#!/bin/sh
out_file="scanner.cpp"
rm compilador
echo gerando scanner.c ...
flex -o scanner.cpp scanner.l
cat scanner.cpp > lex.yy.cpp
sed 's/extern int yylex (void);/\/\/caso queira usar c++\
#ifdef __cplusplus\
    extern "C" int yylex (void);\
#else\
    extern int yylex (void);\
#endif/g' lex.yy.cpp > scanner.cpp
rm lex.yy.cpp
echo gerando parser ...
bison -d parser.y
echo gerando objetos para compilacao ...
#rm parser.tab.o
g++ -c main.cpp scanner.cpp parser.tab.c tiny/util.c tiny/analyze.c tiny/symtab.c tiny/code.c tiny/cgen.c
echo compilando objetos ...
g++ -o compilador main.o scanner.o parser.tab.o util.o analyze.o symtab.o cgen.o code.o -ly -lfl
rm *.o 

# separação do conteúdo dos arquivos
python3 separador_arquivo.py

# remoção do ultimo caractere
head -n -1 conteudo1.txt > temp.txt ; mv temp.txt conteudo1.txt
head -n -1 conteudo2.txt > temp.txt ; mv temp.txt conteudo2.txt

read -p "Do you want to apply preemption? [Y/n] " VAR1
VAR2="Y"

if [[ "$VAR1" == "$VAR2" ]]; then
    python3 OS_generator.py
    cat funcoes1.txt funcoes2.txt main.txt variaveis1.txt variaveis2.txt temp_conteudo.txt final.txt> operationalSys.txt
    #rm temp_conteudo.txt
else
    cat funcoes1.txt funcoes2.txt main.txt variaveis1.txt variaveis2.txt conteudo1.txt conteudo2.txt final.txt> operationalSys.txt
fi

# remoçõa de arquivos temporários
#rm variaveis1.txt
#rm variaveis2.txt
#rm conteudo1.txt
#rm conteudo2.txt
#rm funcoes1.txt
#rm funcoes2.txt

echo gerando codigo intermediario ...
./compilador operationalSys.txt > saida_operationalSys.txt

echo gerando codigo assembly ...
python3 assembly_generator.py

echo gerando codigo binario ...
python3 binary_generator.py 

echo FIM!