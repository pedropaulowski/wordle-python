import os
from sys import platform
from random import seed
from random import randint
import csv
import uuid
from datetime import date
import glob


def validarPalavra(palavra):
    if len(palavra) != 5:
        return False
    elif palavra.isalpha() is False:
        print("Contém números na palavra")
        return False
    else:
        try:
            data_file = open("palavras-validadas.txt", "r")
            content = data_file.read().split('\n')
            if palavra.upper() in content:
                return True
            else:
                return False
        except FileNotFoundError:
            print("Arquivo de palavras não encontrado")
        finally:
            data_file.close()
    
def limparTerminal():
    if platform.startswith("win"):
        os.system('cls')
    else:
        os.system('clear')

def sortearPalavra():
    try:
        data_file = open("palavras-validadas.txt", "r")
        content = data_file.read().split('\n')
        print(f'QUANTIDADE DE PALAVRAS: {len(content)}\n')
        randomNumber = randint(0, len(content))
        print(f'PALAVRA SORTEADA: {content[randomNumber]}')
        return content[randomNumber]
    
    except FileNotFoundError:
        print("Arquivo de palavras não encontrado")
    finally:
        data_file.close()

def mostrarTentativas(palavras, palavraSorteada):
    certo = '+'
    errado = "-"
    meiocerto = '+/-'
    
    print("TENTATIVAS:")
    
    for palavra in palavras:
        palavra = palavra.upper()
        
        for letra in palavra:
            print(f'{letra:^5}', end="")
        
        print() 
        
        for letra in palavra:
            if letra.upper() in palavraSorteada and palavra.index(letra) == palavraSorteada.index(letra):
                print(f'{certo:^5}', end="")
            elif letra in palavraSorteada and palavra.index(letra) != palavraSorteada.index(letra):
                print(f'{meiocerto:^5}', end="")
            else:
                print(f'{errado:^5}', end="")
        
        print("\n")
        
def menuRegras():
    
    print("REGRAS")
    print("1ª: VOCÊ TEM 6 TENTATIVAS.")
    print("2ª: CADA UMA DELAS DEVE SER UMA PALAVRA QUE EXISTA.")
    print("3ª: ACENTOS E CEDILHA SÃO CONSIDERADOS INVÁLIDOS.")
    print()
    print("1 - VOLTAR AO MENU PRINCIPAL")
    print("0 - SAIR")
    
    try:
        val = int(input("Digite o número da opçao que deseja: "))
        
        match val:
            case 1: 
                return
            case 0:
                exit()
            case _:
                limparTerminal()
                print("Essa opção não existe!")
                menuRegras()
    except ValueError:
        limparTerminal()
        print("Opção inválida")
        menuRegras()
    except KeyboardInterrupt:
        exit()
         
class Jogo:
    def __init__(self, palavraSorteada, palavrasTentadas, vidas, id):
        self.palavraSorteada = palavraSorteada
        self.palavrasTentadas = palavrasTentadas
        self.vidas = vidas
        self.id = id
        

def novoJogo(jogo: Jogo = None):
    palavraSorteada = sortearPalavra() if jogo is None else jogo.palavraSorteada
    palavrasTentadas = [] if jogo is None else jogo.palavrasTentadas
    vidas = 6 if jogo is None else jogo.vidas
    gameId = uuid.uuid4() if jogo is None else jogo.id
   
    while True:
        print(f'TENTATIVAS RESTANTES: {vidas}')
        print("1 - CONSUMIR 1 TENTATIVA")
        print("2 - SALVAR ESTADO DO JOGO")
        print("3 - VOLTAR AO MENU PRINCIPAL")
        print("0 - SAIR")

        try:
            val = int(input("Digite o número da opção que deseja: "))
            match val:
                case 1:
                    if vidas > 0:
                        palavra = input("Digite uma palavra de 5 letras: ")
                        if validarPalavra(palavra) is True:
                            vidas = vidas - 1
                            palavrasTentadas.append(palavra)
                            limparTerminal()
                            mostrarTentativas(palavrasTentadas, palavraSorteada)
                            
                            if palavra.upper() == palavraSorteada:
                                print(f"PARABÉNS VOCÊ ACERTOU A PALAVRA SORTEADA!")
                                vidas = 0
                            elif vidas == 0:
                                print(f"VOCÊ PERDEU! A PALAVRA A SER DESCOBERTA ERA: {palavraSorteada}")
                        
                        else:
                            limparTerminal()
                            print("A PALAVARA INSERIDA É INVÁLIDA\n")
                    else:
                        limparTerminal()
                        print(f"VOCÊ NÃO TEM TENTATIVAS RESTANTES! A PALAVRA A SER DESCOBERTA ERA: {palavraSorteada}")
                case 2:
                    arq = "./saves/"+format(gameId)+".csv"
                    try:
                        new_file = open(arq, "w+")
                        new_file.write("data,id,sorteada,vidas,tentadas\n")
                        data = date.today()
                        new_file.write(format(data) + ",")
                        new_file.write(format(gameId) + ",")
                        new_file.write(palavraSorteada + ",")
                        new_file.write(format(vidas) + ",")
                        
                        i = 0
                        for palavra in palavrasTentadas:
                            if i == len(palavrasTentadas) - 1:
                                new_file.write(palavra.upper())
                            else:
                                new_file.write(palavra.upper() + " ")
                            i = i + 1
                
                    except FileExistsError:
                        print("Erro ao criar o arquivo")
                    finally:
                        new_file.close()
                case 3:
                    limparTerminal()
                    return
                case 0:
                    exit()   
                case _:
                    print("Valor fora do intervalo")   
        except ValueError:
            limparTerminal()
            print(f"\nValor inválido, digite um valor válido!")
        except KeyboardInterrupt:
            exit()
            
def read_csv(file):
    with open(file, 'r') as f:
        reader = csv.DictReader(f)
        data = [row for row in reader] 
    return data

while True:
    limparTerminal()
    print("1 - NOVO JOGO")
    print("2 - CONTINUAR JOGO SALVO")
    print("3 - REGRAS")
    print("4 - CONFIGURAÇÕES\n")
    print("0 - SAIR")

    try:
        val = int(input("Digite o número da opção que deseja: "))
        match val:
            case 1:
                limparTerminal()
                novoJogo()
            case 2:
                limparTerminal()
                arquivos = glob.glob("./saves/*.csv")
                i = 1
                jogos = []
                for arq in arquivos:
                    data = read_csv(arq)
                    jogos.append(data)
                    print(f"{i} - Jogo: {data[0]['id'][:8]} - Data: {data[0]['data']} - Tentativas Restantes: {data[0]['vidas']}")
                    i += 1
                
                print(f"0 - VOLTAR AO MENU PRINCIPAL")
                try:
                    i = int(input("Digite o número do jogo que deseja carregar: "))
                    print(f"opcao escolhida {i}")
                    
                    if i == 0:
                        continue
                    
                    i = i - 1

                    if i in range(len(jogos)):
                        # print(jogos[i])
                        
                        # print(jogos[i][0]['tentadas'])
                        
                        n_jogo = Jogo(jogos[i][0]['sorteada'], 
                                      jogos[i][0]['tentadas'].split(" "),
                                      int(jogos[i][0]['vidas']),
                                      jogos[i][0]['id']
                                      )
                        limparTerminal()
                        novoJogo(n_jogo)
                        
                except ValueError:
                    print("Valor digitado é inválido!")
                except KeyboardInterrupt:
                    exit()
                
                
            case 3:
                limparTerminal()
                menuRegras()
            case 0:
                break;          
            case _:
                print("Valor fora do intervalo")
    except ValueError:
        print(f"Valor inválido menu")
    except KeyboardInterrupt:
        exit()
    
    
    
    
    