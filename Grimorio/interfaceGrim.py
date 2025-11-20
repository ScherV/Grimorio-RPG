import flet as ft
import requests

BASE_URL = "http://127.0.0.1:5000"

def main(page: ft.Page):
   
    page.title = "Carregando..."
    page.theme_mode = ft.ThemeMode.DARK
    page.window_width = 450
    page.window_height = 800
    page.bgcolor = "#1a1a2e"
    page.horizontal_alignment = "center"

    
    lbl_titulo = ft.Text("Grimório RPG", size=30, weight="bold", color="purple")
    txt_nome_hab = ft.TextField(label="Nova Habilidade", expand=True, color="white", border_color="purple")
    coluna_habilidades = ft.Column(scroll="auto", expand=True)
    
    txt_input_nome = ft.TextField(label="Nome do Herói", autofocus=True)
    
    def mostrar_msg(texto, cor="green"):
        snack = ft.SnackBar(content=ft.Text(texto, color="white"), bgcolor=cor, duration=3000)
        page.overlay.append(snack)
        snack.open = True
        page.update()

    def definir_nome_personagem(e):
        novo_nome = txt_input_nome.value
        if novo_nome:
            try:
                requests.post(f"{BASE_URL}/nome", json={"nome": novo_nome})
                modal_nome.open = False 
                page.update()
                carregar_dados_iniciais() 
            except Exception as erro:
                mostrar_msg(f"Erro ao salvar nome: {erro}", "red")
        else:
            txt_input_nome.error_text = "Digite um nome!"
            txt_input_nome.update()

   
    modal_nome = ft.AlertDialog(
        modal=True, 
        title=ft.Text("Bem-vindo, Aventureiro!"),
        content=ft.Column([
            ft.Text("Como devemos te chamar?"),
            txt_input_nome
        ], height=100),
        actions=[
            ft.ElevatedButton("Salvar Nome", on_click=definir_nome_personagem, bgcolor="purple", color="white")
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    page.dialog = modal_nome

    def carregar_dados_iniciais():
        print("🔄 Buscando dados na API...") 
        try:
            res = requests.get(f"{BASE_URL}/perfil")
            
            if res.status_code == 200:
                dados = res.json()
                nome_personagem = dados.get("nome_personagem", "Viajante")
                
               
                print(f"👤 Nome recebido: {nome_personagem}") 
                lbl_titulo.value = f"Grimório de {nome_personagem}"
                page.title = f"Grimório de {nome_personagem}"
                
                
                if nome_personagem == "Viajante":
                    print("⚠️ Nome é padrão. Tentando abrir modal...")
                    page.open(modal_nome)
                
                else:
                    print("✅ Nome já definido. Modal permanece fechado.")

                renderizar_lista(dados.get("habilidades", {}))
            
            page.update()
            
        except Exception as e:
            print(f"❌ Erro de conexão: {e}")
            mostrar_msg(f"Erro de conexão: {e}", "red")

    def renderizar_lista(dict_habilidades):
        coluna_habilidades.controls.clear()
        if not dict_habilidades:
            coluna_habilidades.controls.append(ft.Container(content=ft.Text("Nenhuma habilidade...", color="grey"), alignment=ft.alignment.center))
            return

        for nome, nivel in dict_habilidades.items():
            def deletar(e, n=nome):
                requests.delete(f"{BASE_URL}/habilidades/{n}")
                carregar_dados_iniciais()
            
            def upar(e, n=nome):
                res = requests.put(f"{BASE_URL}/habilidades/{n}")
                if res.status_code == 200:
                    mostrar_msg(f"{n} subiu de nível!", "green")
                    carregar_dados_iniciais()
                else:
                    erro = res.json().get("detalhe") or res.json().get("erro")
                    mostrar_msg(erro, "red")

            card = ft.Container(
                bgcolor="#16213e", border_radius=10, padding=10, margin=ft.margin.only(bottom=5),
                content=ft.Row([
                    ft.Row([
                        ft.Icon(ft.Icons.BOLT, color="yellow"),
                        ft.Column([
                            ft.Text(nome.title(), weight="bold", size=16),
                            ft.Text(f"Nível {nivel}", color="cyan", size=12)
                        ], spacing=2)
                    ]),
                    ft.Row([
                        ft.IconButton(icon=ft.Icons.ARROW_UPWARD, icon_color="green", on_click=upar),
                        ft.IconButton(icon=ft.Icons.DELETE, icon_color="red", on_click=deletar)
                    ])
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
            )
            coluna_habilidades.controls.append(card)

    def adicionar(e):
        if txt_nome_hab.value:
            requests.post(f"{BASE_URL}/habilidades", json={"nome": txt_nome_hab.value})
            txt_nome_hab.value = ""
            carregar_dados_iniciais()

    btn_add = ft.Container(
        content=ft.Icon(ft.Icons.ADD, color="white"), bgcolor="purple", padding=10, border_radius=10,
        on_click=adicionar, ink=True
    )

    page.add(
        ft.Container(content=lbl_titulo, alignment=ft.alignment.center, margin=20),
        ft.Row([txt_nome_hab, btn_add]),
        ft.Divider(color="grey"),
        coluna_habilidades
    )

    carregar_dados_iniciais()

ft.app(target=main)