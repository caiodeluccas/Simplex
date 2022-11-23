# Simplex Tabelado
# Alunos:
# Caio de Luccas Rosolen
# Rodrigo Tugores
# Programação Linear Segundo Semestre 2022 turma de ADS manhã da Fatec de Americana
# 
#from operator import index
from os import system
from numpy import array, double, eye, integer, negative
import numpy as np


class SimplexTabelado:

    def __init__(self):

        self.tabelaOriginal = []
    
    # fo é a função objetivo
    def funcaoObjetivo(self, fo: list): 

        self.tabelaOriginal.append(fo)

    # criar restrições
    def restricoes(self, sa: list):

        self.tabelaOriginal.append(sa)


    # coluna que entra
    def colunaQEntra(self) -> int: # retorna um inteiro

        coluna = min(self.tabelaOriginal[0])
        index = self.tabelaOriginal[0].index(coluna)

        return index
    
    # linha que sai
    def linhaQSai(self, coluna_entra: int) -> int:

        guardaResultado = {}
        for i in range(len(self.tabelaOriginal)):
            if i > 0:
                if self.tabelaOriginal[i][coluna_entra] > 0: 
                    pega = self.tabelaOriginal [i][-1] / self.tabelaOriginal[i][coluna_entra]
                    guardaResultado[i] = pega
        index = min(guardaResultado, key=guardaResultado.get)    

        return index
        
    # 6 - calcular a nova linha pivo
    def calculaNovaPivo(self, coluna_entra: int, linha_sai: list) -> list:

        linha = self.tabelaOriginal[linha_sai]
        pivo = linha[coluna_entra]
        novaLinhaPivo = [value / pivo for value in linha]

        return novaLinhaPivo

    
    # 7 Calcular as novas linhas
    def calculaNovaLinha(self, linha: list, coluna_entra: int, linha_pivo: list) -> list:
        # pega a nova linha pivo e multiplica pelo elemento da coluna que entra com o sinal trocado
        pivo = linha[coluna_entra] * -1
        # multiplica a linha pivo 
        linha_resultante = [value * pivo for value in linha_pivo] # igual ao for normal
        # cria a lista com as novas linhas calculadas
        nova_linha = []
        for i in range(len(linha_resultante)):
            #soma a linha calculada com a linha 
            soma = linha_resultante[i] + linha[i]
            nova_linha.append(soma)

        return nova_linha

   
    # para cada elemento da primeira linha verifica se é menor que zero. 
    def negativo(self) -> bool: 
        negativo = list(filter(lambda x: x < 0, self.tabelaOriginal[0]))

        return True if len(negativo) > 0 else False

    
    # definir as variáveis que entram nas funções
    def variaveis(self):

        coluna_entra = self.colunaQEntra()
        primeiraLinhaQSai = self.linhaQSai(coluna_entra)
        linha_pivo = self.calculaNovaPivo(coluna_entra, primeiraLinhaQSai)
        self.tabelaOriginal[primeiraLinhaQSai] = linha_pivo
        copiaTabela = self.tabelaOriginal.copy() # clone da tabela original

        index = 0

        # looping que monta a tabela resultante
        while index < len(self.tabelaOriginal):
            if index != primeiraLinhaQSai:
                linha = copiaTabela[index]
                nova_line = self.calculaNovaLinha(linha, coluna_entra, linha_pivo)
                self.tabelaOriginal[index] = nova_line
            index += 1
    
    # mostrar a nova tabela sem negativos na primeira linha - tabela final
    def imprimeTabela(self):
        for i in range(len(self.tabelaOriginal)):
            for j in range(len(self.tabelaOriginal[0])):
                print(f"{self.tabelaOriginal[i][j]}\t", end="")
            print()


    def imprimeSolucaoOtima(self):
        
        somaColunas = np.sum(self.tabelaOriginal, axis=0, dtype=double)
               
        #print(f'Soma do elements das colunas é {somaColunas}')
   
        # Conta quantos zeros possui cada coluna da tabela final
        pegaZeros =[]
        for i in range(len(self.tabelaOriginal[0])):
            contazeros = 0
            for j in range(len(self.tabelaOriginal)):
                if self.tabelaOriginal[j][i] == 0:
                    contazeros = contazeros + 1
            pegaZeros.append(contazeros)

        # pega os valores de b que corresponde aos resultados das variáveis básicas        
        pegaResultadoB = []
        pegaColuna = []  
        for i in range(len(self.tabelaOriginal)):
            for j in range(len(self.tabelaOriginal[0])):
                if self.tabelaOriginal[i][j] == 1 and somaColunas[j] == 1 and pegaZeros[j] == numeroRestricoes:
                    pegaColuna.append(j)
                    pegaResultadoB.append(self.tabelaOriginal[i][-1])  
     
        print()    
        print("********** Solução **********")
        print()                  
        
        if pegaResultadoB[0] == 0:
            print("O valor da Maximização de Z é 0")
            print()
        else:
            print("*** Variáveis básicas *** \t")    
            for i in pegaColuna:
                j=pegaColuna.index(i)
                if i != 0:
                    print('A variável ' +  str(cabecalho[i]) + ' é = ' + str(pegaResultadoB[j]))
            print()
            print("*** Variáveis NÃO básicas *** \t") 
            pegaColuna2 = []
            cont = 0
            for i in pegaZeros:
                if i != numeroRestricoes:
                    pegaColuna2.append(cont)
                cont = cont + 1
                   
            for i in pegaColuna2:
                if i != len(somaColunas)-1:
                    print('A variável ' +  str(cabecalho[i]) + ' é = 0')
            print()
            print("O valor da Maximização de Z é", pegaResultadoB[0])
            print()
            system("pause")
                

    def resolve(self):
        self.variaveis()

        while self.negativo():
            self.variaveis()

        self.imprimeTabela()
        self.imprimeSolucaoOtima()

if __name__ == '__main__':
        
    simplex = SimplexTabelado()
    
    print("********** -> ENTRADA DOS DADOS <- **********")
    print()
  
    cabecalho = ["Z"]
    print()
    while True:
        try:
            numeroVariaveis = int(float(input("Qual o número da variáveis do problema?  ")))
            break
        except ValueError:
            print('Não foi digitado nenhum número!')
    print()
    while True:
        try:
            numeroRestricoes = int(input("Qual o número de restrições? "))
            break
        except ValueError:
            print('Não foi digitado nenhum número!')

    print()
    print("--------Entre com as informações da função objetivo-------------")
    lista1 = [1]
    for i in range(numeroVariaveis):
        print()
        while True:
            try:
                valor = float(input(" Variável X%d da função objetivo: " % (i+1)))
                break
            except ValueError:
                print('Não foi digitado nenhum número!')

        lista1.append(valor*-1)
            
        cabecalho.append("%s%s" % ("X",i+1))
    
      
    lst_zeros = [0 for i in range(0, numeroRestricoes+1)]
    print("A lista 1 contém: ", lista1 + lst_zeros)
    simplex.funcaoObjetivo(lista1 + lst_zeros)

    # Restrições  
    print()
    print()
    print("------------Entre com as informações das restições------------------")   
    print()  
    x=0    
    while x < (numeroRestricoes):
        cabecalho.append("%s%s" % ("F",x+1))
        lista2 = [0]
        print()
        print("Restrição", x+1)
        for i in range(numeroVariaveis):
            while True:
                try:
                    valorVariavel = float(input(" Valor da variável X%d : " % (i+1)))
                    break
                except ValueError:
                    print('Não foi digitado nenhum número')
            lista2.append(valorVariavel)
        

        for i in range(numeroRestricoes):


            if i == x:
                lista2.append(1)

            else:
                lista2.append(0)
        while True:
            try:
                valorB = float(input("Valor de b:  "))
                break
            except ValueError:
                print('Não foi digitado nenhum número!')
        lista2.append(valorB)

            
        x+=1
        
        simplex.restricoes(lista2) 
        print("Lista ",lista2)     

    # criar o cabeçalho da tabela   
    cabecalho.append("B")
    print()
    print("*--------Tabela Final--------*")
    print(cabecalho)
    
    simplex.resolve()
