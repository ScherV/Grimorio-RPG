import os 
import json
os.system('cls')
ARQUIVO_DB = "personagem.json"

def carregarDados():
    try:
        with open(ARQUIVO_DB, "r") as arquivo:
            data = json.load(arquivo)
            return data
    except FileNotFoundError:
        return {}
    
def salvarDados(habilidades):
    with open(ARQUIVO_DB, "w") as arquivo:
        json.dump(habilidades, arquivo, indent=4)

def excluirhabilidade():
    print("\n----- GERENCIAR EXCLUSÃO -----")

    if not habilidades:
        print("\nSeu repertório de habilidades já está vazio!")
        return
    
    while True:

        print("1 - Excluir UMA habilidade específica")
        print("2 - Excluir TODAS as habilidades")
        print("0 - Cancelar")
    
        opcao = input("Escolha uma das opções acima: ")

        if opcao == "1":
            while True:
                nome = input("\nDigite o nome da habilidade que deseja excluir: ")

                if nome in habilidades:
                    del habilidades[nome]
                    salvarDados(habilidades)
                    print(f"\nHabilidade '{nome}' removida com sucesso!")
                    return
                
                elif nome == "cancelar":
                    break
                    
                else:
                    print(f"\nVocê não possui '{nome}' no seu repertório, ou escreveu errado amigão...")
                    print("Digite 'cancelar' se deseja voltar.")

        elif opcao == "2":
            while True:
                confirmacao = input("\nTem certeza ? isso apagará todas as suas habilidades PRA SEMPRE! (s/n) ")

                if confirmacao == "s":
                    habilidades.clear()
                    salvarDados(habilidades)
                    print("\nTodas as suas habilidades foram excluídas!")
                    return

                elif confirmacao == "n":
                    print("\nOperação Cancelada!\n")
                    break
                
                else:
                    print("\nDigite 's' para SIM e 'n' para NÃO")
                
        elif opcao == "0":
            print("\nVoltando ao menu...")
            return

        else:
            print("\nOpção inválida.")

habilidades = carregarDados()

def verHabilidades(habilidades):
    print("\n-----HABILIDADES-----")
    if habilidades:
        for nomeHab, levelHab in habilidades.items():
            print(f"{nomeHab.title()} | Nível: {levelHab}")
    else:
        print("\nVocê não possui habilidades!")

def adicionarHabilidade(habilidades):
    novaHab = input("\nAdicione sua nova habilidade: ")
    if novaHab in habilidades:
        print(f"\nVocê já possui essa habilidade!")
        return

    habilidades[novaHab] = 1
    salvarDados(habilidades)
    print(f"\nHabilidade '{novaHab}' registrada no nível 1!")

def uparHabilidade(habilidades):
    print("\n----- UPGRADE DE HABILIDADE -----")

    if not habilidades:
        print("\nVocê ainda não possui habilidades para upar!")
        print("Você precisa ter pelo menos 1 habilidade para subir de nível")
        return

    uparHab = input("Qual habilidade deseja subir de nível (+1) ? \n")

    if uparHab not in habilidades:
        print("\nOu você ainda não aprendeu essa habilidade, ou escreveu errado amigão...")
        return
    
    nivelAtual = habilidades[uparHab]
    novoNivel = nivelAtual + 1

    menorNivel = min(habilidades.values())
    diferencaMaxima = 1

    if (novoNivel - menorNivel) > diferencaMaxima:
        print("\n--- REQUISITO DE EQUILIBRIO ---\n")
        print(f"Você não pode deixar suas habilidades muito pra trás!")
        print(f"Sua habilidade mais fraca está no nivel {menorNivel}. ")
        print(f"Para upar '{uparHab}' para o nível {novoNivel}, todas as outras devem ser pelo menos nível {novoNivel - diferencaMaxima}.")
        return
    
    habilidades[uparHab] = novoNivel
    salvarDados(habilidades)
    print(f"\n Parabéns! Habilidade '{uparHab}' atualizada para o nível: {novoNivel}.")

def menuPrincipal():
    while True:

        menu = (
        "\n----- MENU -----\n"
        "1 - Adicionar Habilidade\n"
        "2 - Ver Habilidades\n"
        "3 - Upar Habilidades\n"
        "4 - Excluir Habilidades\n"
        "0 - sair\n"
        "\nSelecione uma opção: "
    )
        comando = input(menu)

        if comando == "1":
            adicionarHabilidade(habilidades)
        elif comando == "2":
            verHabilidades(habilidades)
        elif comando == "3":
            uparHabilidade(habilidades)
        elif comando == "4":
            excluirhabilidade()
        elif comando == "0":
            break
        else:
            print("Digite uma opção válida!")

menuPrincipal()

print("Programa Finalizado.")