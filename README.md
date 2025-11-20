# 🔮 Grimório RPG

> Um sistema Full Stack para gerenciamento de habilidades de RPG com regras de progressão balanceada.

Este projeto é uma aplicação completa que demonstra a arquitetura **Cliente-Servidor**, utilizando uma **API REST** para lógica de negócios e persistência, e uma **Interface Gráfica (GUI)** moderna para interação do usuário.

## 🛠️ Tecnologias Utilizadas

* **Linguagem:** Python 3.14
* **Backend (API):** Flask
* **Frontend (GUI):** Flet (Framework Python para UI)
* **Comunicação:** Requests (HTTP)
* **Banco de Dados:** JSON (Persistência de Arquivo)

## ⚙️ Funcionalidades

-   **CRUD Completo:** Adicionar, Ler, Atualizar e Deletar habilidades.
-   **Sistema de Perfil:** O sistema reconhece o nome do personagem ou solicita criação de um novo.
-   **Persistência de Dados:** Todo o progresso é salvo automaticamente em `personagem.json`.
-   **Regra de Negócio Complexa (Pirâmide de Níveis):**
    -   O sistema impede que o jogador evolua uma habilidade isoladamente.
    -   *Lógica:* Para subir uma habilidade para o nível `X`, é necessário ter pelo menos **2 outras habilidades** no nível `X-1` (ou superior) para dar suporte.
    -   Isso garante um crescimento equilibrado do personagem.

## 🚀 Como Rodar o Projeto

Siga os passos abaixo para executar o sistema na sua máquina:

### 1. Pré-requisitos
Certifique-se de ter o Python instalado. Instale as dependências do projeto:

```bash
pip install flask flet requests

# Entre na pasta do projeto
cd grimorio

# Rode a API
python API_RPG.py

# Mantenha o terminal da API aberto. Abra um segundo terminal e rode a interface
cd grimorio
python interfaceGrim.py

** Estrutura do Projeto

API_RPG.py: O cérebro do sistema. Contém as rotas Flask, a lógica de validação da "Pirâmide" e manipulação do JSON.

interfaceRPG.py: A interface visual feita em Flet. Gerencia os inputs, botões e feedback visual (SnackBars).

personagem.json: O arquivo onde os dados são persistidos.