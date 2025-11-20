from flask import Flask, jsonify, request
import json
import os

app = Flask(__name__)
ARQUIVO_DB = "personagem.json"


def carregar_dados_completos():
    
    estrutura_padrao = {"nome_personagem": "Viajante", "habilidades": {}}
    
    if not os.path.exists(ARQUIVO_DB):
        return estrutura_padrao
    try:
        with open(ARQUIVO_DB, "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)
           
            if "habilidades" not in dados:
                return estrutura_padrao
            return dados
    except Exception:
        return estrutura_padrao

def salvar_dados_completos(dados):
    with open(ARQUIVO_DB, "w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, indent=4)



@app.route('/')
def home():
    return "<h1>🛡️ API do RPG Online!</h1>"


@app.route('/perfil', methods=['GET'])
def get_perfil():
    dados = carregar_dados_completos()
    return jsonify(dados)


@app.route('/nome', methods=['POST'])
def set_nome():
    info = request.get_json()
    novo_nome = info.get('nome')
    
    dados = carregar_dados_completos()
    dados['nome_personagem'] = novo_nome
    salvar_dados_completos(dados)
    
    return jsonify({"mensagem": f"Bem-vindo, {novo_nome}!"}), 200


@app.route('/habilidades', methods=['GET'])
def listar_habilidades():
    dados = carregar_dados_completos()
    return jsonify(dados["habilidades"])

@app.route('/habilidades', methods=['POST'])
def adicionar_habilidade_api():
    req_data = request.get_json()
    nova_hab = req_data.get('nome')
    
    if not nova_hab: return jsonify({"erro": "Nome inválido"}), 400

    dados = carregar_dados_completos()
    habilidades = dados["habilidades"]
    
    if nova_hab in habilidades: return jsonify({"erro": "Habilidade já existe"}), 409

    habilidades[nova_hab] = 1
    dados["habilidades"] = habilidades 
    salvar_dados_completos(dados) 
    
    return jsonify({"mensagem": "Criado!"}), 201

@app.route('/habilidades/<nome>', methods=['DELETE'])
def deletar_habilidade(nome):
    dados = carregar_dados_completos()
    habilidades = dados["habilidades"]
    
    if nome in habilidades:
        del habilidades[nome]
        dados["habilidades"] = habilidades
        salvar_dados_completos(dados)
        return jsonify({"mensagem": "Deletado!"}), 200
    return jsonify({"erro": "Não encontrado"}), 404

@app.route('/habilidades/<nome>', methods=['PUT'])
def upar_habilidade_api(nome):
    try:
        dados = carregar_dados_completos()
        habilidades = dados["habilidades"]

        if nome not in habilidades: return jsonify({"erro": "Não encontrado"}), 404

        nivel_atual = habilidades[nome]
        novo_nivel = nivel_atual + 1
        
        qtd_necessaria = 2
        contador_requisitos = 0
        for hab_nome, hab_nivel in habilidades.items():
            if hab_nome != nome and hab_nivel >= nivel_atual:
                contador_requisitos += 1

        if contador_requisitos < qtd_necessaria:
            return jsonify({
                "erro": "Bloqueio de Evolução",
                "detalhe": f"Para ir ao Nível {novo_nivel}, tenha outras {qtd_necessaria} habilidades no nível {nivel_atual}+."
            }), 400

        habilidades[nome] = novo_nivel
        dados["habilidades"] = habilidades
        salvar_dados_completos(dados)
        return jsonify({"mensagem": "Level Up!"}), 200

    except Exception as e:
        return jsonify({"erro": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)