import ias_functions as ias
import arquivo as arq
import memoria as mem



#Ler um arquivo txt e passar uma lista para a classe memória
memoria_ias = mem.Memoria( arq.txt_toList() )

#cria o simulador com a memória criada acima
computador = ias.process(memoria_ias)

#Executa as instruções
computador.run()

#Salva em um arquivo memoria_final.txt o estado final da memória 
arq.salvar_memoria(computador)
