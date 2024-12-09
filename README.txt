### Grupo: SO-TI-02
# Aluno 1: André Alexandre (fc62224)
# Aluno 2: Sofian Fathallah (fc62814)
# Aluno 3: Tair Injai (fc62848)



### Exemplos de comandos para executar o pwordcount:
1) ./pword -m c -p 7 -i 1 -d count -w our file2.txt
2) ./pword -m l -p 1 -i 3 -d count -w ball file1.txt
3) ./pword -m i -p 4 -w fire file2.txt file3.txt
4) ./pword -m c -p 3 -i 0.1 -d see -w our file1.txt file2.txt file3.txt
5) ./pword -m l -p 5 -i 2 -d be -w say file3.txt
6) ./pword -m i -p 2 -i 1 -d count file2.txt
7) ./pword -m c -p 5 -i 0.001 -w our file1.txt
8) ./pword -m l -p 1 -i 1 -d count -w our file2.txt file1.txt
9) ./pword -m i -p 1 -i 1 -d count -w our file2.txt



### Limitações da implementação:

- Por vezes, não é possível visualizar a progressão dos Resultados Parciais Temporizados, 
pois os processos são mais rápidos do que o intervalo definido. Isso dá-se principalmente nos modos
L e I devido ao "totalQ" e ao "sumQ".

- Por vezes, no modo L, a contagem Queue possui perdas. E, uma vez que o Queue já possui mecanismos 
transparentes de sincronização, não fazemos ideia do que possa ser o motivo senão algo 
relacionado com o próprio set().




### Outras informações pertinentes:

- À parte do Value devidamente especificado no enunciado, também fizemos uso de um Value parar
guardar o ficheiro ou bloco de dados onde o programa se escontra.

- Como não conseguimos adicionar mais de uma mensagem ao Queue, temos uma lista que é atualizada a 
cada mensagem que o Queue recebe de modo a guardar as mensagens e as poder analisar mais tarde no
decorrer do programa

