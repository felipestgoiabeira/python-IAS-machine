class Memoria():
    def __init__(self, lista):
        self.memoria = [x for x in range(0,1000)]
        index = 0
        for dado in lista:
            self.memoria[index] = dado
            index += 1

    # setWord recebe o endereço da memoria, 
    # representado por um inteiro e o valor para guarda neste endereço
    def setWord(self,adress, value):
        index = int(adress,2)
        self.memoria[index] = value
    
    #getWord recupera o valor em um endereço
    def getWord(self, adress):
        index = int(adress,2)
        return self.memoria[index]
    
    #APAGAR
    def getValue(self, adress):
        return self.memoria[adress][1:41]