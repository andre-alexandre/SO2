### Grupo: SO-TI-02
# Aluno 1: André Alexandre (fc62224)
# Aluno 2: Sofian Fathallah (fc62814)
# Aluno 3: Tair Injai (fc62848)



### Exemplos de comandos para executar o pwordcount:
1) ./pword -m c -p 1 -w our file2.txt
2) ./pword -m l -p 3 -w ball file1.txt file3.txt
3) ./pword -m i -p 2 -w win file2.txt file3.txt file4.txt
4) ./pword -p 7 -w sick file1.txt
5) ./pword -w we file2.txt
6) ./pword -w thanks file1.txt file3.txt
7) ./pword -m -p 3 -w like file2.txt 
8) ./pword -m l -p 4 file2.txt 



### Limitações da implementação:

- Função parse_arguments: A funcionalidades da função parse_arguments,
ao invés de terem sido aplicadas no ficheiro python, deveriam ter 
sido realizadas no ficheiro bash.

- Divisão por Linhas em Partes Iguais: O programa divide 
as linhas de arquivo igualmente entre processos. No entanto, caso 
existam poucas linhas e apenas uma ou duas dessas linhas sejam grandes
e contenham em grande quantidade a palavra que se procura, pode criar-se 
uma grande disparidade entre o tempo e trabalho exercidos por cada processo.



### Abordagem para a divisão dos ficheiros:

- Divisão por Linhas: No caso de um único ficheiro, 
ele é dividido em partes uniformes com base no número 
de linhas e no número de processos com a ajuda da 
função split_file. Isso significa que cada processo 
recebe aproximadamente o mesmo número de linhas. 
Essa abordagem ajuda a distribuir o trabalho de 
cada processo de forma rápida e eficiente.

- Divisão por Arquivos: No caso de vários ficheiros, criamos 
grupos de ficheiros que serão divididos pelos processos solicitados, 
tal como exemplificado na função distribute. Caso o número de 
processos seja superior ao número de ficheiros, iguala-se os dois 
antecipadamente na função main, de modo a que cada grupo de ficheiros
tenha apenas um ficheiro para ser atribuído a um processo. Caso o número 
de processos seja inferior ao de ficheiros, será feita uma divisão dos grupos
de ficheiros de modo a que cada processos seja responsável por um número de
ficheiros semelhante aos restantes processos, de modo a não haver grandes 
disparidades de número de ficheiros por processo



### Outras informações pertinentes:

- Não existe sincronização entre os processos, o que faz com que processos 
que começaram mais tarde possam devolver o seu resultado mais cedo; ou seja,
que os resultados não sejam devolvidos de forma ordenada.
