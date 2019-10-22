import glob
from numpy import binary_repr
import memoria as mem


class process():
    
    #word = Word()
    left_instruction = True
    MBR = str()
    MQ = str()
    adress = 1
    PC = binary_repr(0,40) 
    MAR = str() 
    IBR = str()
    IR = str()
    AC = str()

    #a função recebe um string, 
    #verifica o bit de sinal e retorna o inteiro correspondente

    def imprimir(self):
        print('PC: %s' %self.printRes(self.PC) )
        print('MBR: %s' %self.printRes(self.MBR) )
        print('IBR: %s' %self.printRes(self.IBR) )
        print('IR: %s' %self.printRes(self.IR) )
        print('MAR: %s' %self.printRes(self.MAR) )
        print('AC: %s' %self.printRes(self.AC) )
        print('MQ: %s' %self.printRes(self.MQ) )
        
    def printRes(self, registrador):
        if len(registrador) == 0: return 'vazio'
        else: return registrador

    def toInt(self,string):
        if string[0] == '1': return - int( string[1:], 2) 
        return int(string, 2)
    
    def toBin40(self, num):

        string = binary_repr(num)
        sinal = ''

        if string[0] == '-':
            sinal = '1'
            tam = len(string[1:])
            x = '0'
            zeros = [x for i in range(40-tam-1)]
            newString = str(sinal) + ''.join(zeros) + string[1:]
            return newString
            
        else: 
            sinal = '0'
            tam = len(string[1:])
            x = '0'
            zeros= [x for i in range(40-tam)]
            newString = sinal + ''.join(zeros) + string
            return newString

    # Executa o ciclo de busca, execução e faz o output pro console
    def run(self):
        count = 1
        while not( True ) == 0 : #int(self.PC, 2)
                print('\n---------------------------------------------\n')
                print('CONTEÚDO DOS REGISTRADORES NO INÍCIO DO CICLO %d\n ' %count)
                print('----------------------------------------------\n')
                self.imprimir() 
    
                self.buscar()
               
                if self.toInt(self.IR) == 0 :
                     print('#############################################\n')
                     print('CONTEÚDO DOS REGISTRADORES NO FINAL DO CICLO %d \n ' %count)
                     print('----------------------------------------------\n')
                     self.imprimir()
                     break

                self.execucao(self.IR, self.MAR)

                print('#############################################\n')
                print('CONTEÚDO DOS REGISTRADORES NO FINAL DO CICLO %d \n ' %count)
                print('----------------------------------------------\n')
                self.imprimir()

                count += 1
                
                

    # CICLO DE BUSCA
    def buscar(self):
        #a próxima instrução está no IBR?
        if len(self.IBR) == 0:
            self.MAR = self.PC 
            self.MBR = self.memoria.getWord( self.MAR )

            if self.left_instruction :
                self.IBR = self.MBR[20 : 40]
                self.IR = self.MBR[0 : 8]
                self.MAR = self.MBR[8 : 20]

            else:
                self.IR = self.MBR[20 : 28]
                self.MAR = self.MBR[28 : 40]
                self.left_instruction = True

        else:
            self.IR = self.IBR[0 : 8]
            self.MAR = self.IBR[8 : 20]
            self.IBR = ''
            self.PC = binary_repr(int(self.PC,2) + 1, 40)
            
    #Executa a operação conforme o número binário em IR  
    def execucao(self, IR, adress):
        self.switcher[IR](adress)

    def loadMQ(self, adress):
        self.AC = self.MQ

    def loadMxtoMQ(self,adress): 
        self.MQ = self.memoria.getWord(adress)

    def stor(self, adress): 
        self.memoria.setWord(adress, self.AC) 

    def transfer_Mx_to_AC(self, adress) :
        self.AC = self.memoria.getWord(adress)

    def transfer_minMx_to_AC(self, adress): 
        num = self.memoria.getWord(adress)
        intNum = - self.toInt(num)
        self.AC = self.toBin40(intNum)
        
    def transfer_absMx_to_AC(self, adress): 
        num = self.toInt( self.memoria.getWord( adress ) )
        self.AC = self.toBin40(abs(num))
    
    def transfer_minAbsMx_to_AC(self,adress):
        num = self.toInt(self.memoria.getWord(adress))
        self.AC = self.toBin40(- abs(num))

    def jumpRight(self, adress): 
        self.IBR = ""
        self.PC = adress
        self.left_instruction = False

    def jumpLeft(self, adress):
        self.IBR = ""
        self.PC = adress
        

    def jumpPosRight(self,adress):
        num =  self.toInt(self.AC)
        if num > 0 : 
            self.IBR = ""
            self.PC = adress

    def jumpPosLeft(self, adress):
        num = self.toInt(self.AC)
        if num > 0 : 
            self.IBR = ""
            self.PC = adress
            self.left_instruction = False

    def add(self, adress): 
        numMX = self.toInt( self.memoria.getWord(adress) )
        numAC = self.toInt(self.AC)
        self.AC = self.toBin40(numMX + numAC)

    def addAbs(self,adress): 
        numMX = self.toInt( self.memoria.getWord(adress) )
        numAC = self.toInt(self.AC)
        self.AC = self.toBin40(abs(numMX)+numAC)

    def sub(self, adress): 
        numMX = self.toInt( self.memoria.getWord(adress) )
        numAC = self.toInt(self.AC)
        self.AC =self.toBin40(numMX - numAC)

    def subAbs(self, adress):
        numMX = self.toInt( self.memoria.getWord(adress) )
        numAC = self.toInt( self.AC )
        self.AC = self.toBin40(abs(numMX)+numAC)

    def mult(self,adress):
         numMX = self.toInt( self.memoria.getWord(adress) )
         numMQ = self.toInt(self.MQ)
         self.AC = self.toBin40(numMQ * numMX)
         self.MQ = self.toBin40(0)

    def div(self, adress):
        numMX = self.toInt( self.memoria.getWord(adress) )
        numAC = self.toInt( self.AC )
        self.memoria.setWord(adress,self.toBin40(numMX / numAC)) 
        self.AC = self.toBin40(numMX % numAC)

    def lsh(self, adress): 
        numAC = self.toBin40(self.AC)
        numAC = numAC >> 1
        self.AC = numAC.bin

    def rsh(self, adress): 
        numAC = self.toInt(self.AC)
        numAC = numAC << 1
        self.AC = self.toBin40(numAC)

    def storRight(self,adress):
        MX = self.memoria.getWord(adress)
        AC = self.AC[26:40] 
        newMX = MX[0:8]+AC+MX[19:40]
        self.memoria.setWord(adress, newMX)

    def storLeft(self, adress): 
        MX = self.memoria.getWord(adress)
        AC = self.AC[26:40] 
        newMX = MX[0:29]+AC
        self.memoria.setWord(adress, newMX)

    def __init__(self, memoria):

        self.memoria = memoria
        
        self.switcher = {
                '00001010' : self.loadMQ, # Transfere o conteúdo do registrador MQ para o acumulador AC
                '00001001' : self.loadMxtoMQ, # Transfere o conteúdo da posição de memória X para MQ
                '00100001' : self.stor, # Transfere o conteúdo do acumulador para a posição de memória X
                '00000001' : self.transfer_Mx_to_AC, # Transfere M(X) para o acumulador
                '00000010' : self.transfer_minMx_to_AC, # Transfere - M(X) para o acumulador
                '00000011' : self.transfer_absMx_to_AC, # Transfere o valor absoluto de M(X) para o acumulador
                '00000100' : self.transfer_minAbsMx_to_AC, # Transfere - IM(X) I para o acumulador
                '00001101' : self.jumpRight, #A próxima instrução a ser executada é buscada na metade esquerda de M(X)
                '00001110' : self.jumpLeft, # A próxima instrução a ser executada é buscada na metade direita de M(X)
                '00001111' : self.jumpPosRight, #Se o número no acumulador é um valor não-negativo, a próxima instrução a ser executada é buscada na metade esquerda de M(X)
                '00010000' : self.jumpPosLeft, #Se o número no acumulador é um valor não-negativo, a próxima instrução a ser executada é buscada na metade direita de M(X)
                '00000101' : self.add, #Soma M(X) a AC; armazena o resultado em AC         
                '00000111' : self.addAbs, #Soma IM(X) I a AC; armazena oresultado em AC
                '00000110' : self.sub, #Subtrai M(X) de AC; armazena o resultado em AC
                '00001000' : self.subAbs, #Subtrai IM(X) I de AC; armazena o resto em AC
                '00001011' : self.mult, #Multiplica M(X) por MQ; armazena os bits mais significativos do resultado em AC, armazena os bits menos significativos em MQ.
                '00001100' : self.div, #Divide AC por M(X); armazena o quociente em MQ e o resto em AC
                '00010100' : self.lsh, #Multiplica o acumulador por 2 (isto é,desloca os bits uma posição para a esquerda).
                '00010101' : self.rsh, #Divide o acumulador por 2 (isto é, desloca os bits uma posição para a direita)
                '00010010' : self.storRight, #Substitui o campo de endereço à esquerda de M(X) pelos 12 bits mais à direita de AC
                '00010011' : self.storLeft, #Substitui o campo de endereço à direita de M(X) pelos 12 bits mais à direita de AC.
            }

    
    
    

 


