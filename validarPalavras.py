def validarPalavras(arquivoInicial):
    try:
        data_file = open(arquivoInicial, "r")
        content = data_file.read().split('\n')
        arquivo_final = escreverNoArquivo()
        for words in content:
            if len(words) == 5:
                arquivo_final.write(words.upper() + "\n")  
    except FileNotFoundError:
        print("Arquivo de palavras não encontrado")

def escreverNoArquivo():
    try:
        new_file = open("palavras-validadas.txt", "w+")
        return new_file
    except FileExistsError:
        print("Erro ao criar o arquivo")

# validarPalavras("br-sem-acentos.txt")
