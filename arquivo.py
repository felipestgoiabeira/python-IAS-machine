import glob

def txt_toList():
    i = 1
    arquivos = []
    print("\nOs arquivos .txt no diretório são:\n")
    for file in glob.glob("*.txt"):
        print("Arquivo %d : %s" % (i, file))
        i += 1
        arquivos.append(file)
    num = int(input("Digite o número do arquivo:"))
    with open(arquivos[num - 1]) as f:
        linhas = f.readlines()
    toList = []
    for i in linhas:
        if i!='\n' :
            #l.append(i[0:len(i)-1]) usar para sem comentários
            toList.append(i[0:40])
    return toList

def salvar_memoria(computador):
    
    memoria =[] 
    for item in computador.memoria.memoria:
        if type(item)==str:
            memoria.append(item)
    with open('memoria_final.txt', 'w') as arquivo:
        
        for item in memoria:
            arquivo.write(item + '\n')