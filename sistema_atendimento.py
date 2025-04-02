import ttkbootstrap as ttk
from PIL import Image, ImageTk
import os
import banco_de_dados  # Importando o módulo de banco de dados


class SistemaAtendimentoApp(ttk.Window):
    def __init__(self):
        super().__init__(themename="darkly")  # Definir o tema no ttkbootstrap
        self.title("Sistema de Atendimento")
        self.geometry("1280x720")
        self.resizable(True, True)

        # Criação do menu lateral com fundo cinza
        self.menu_frame = ttk.Frame(self, width=40, style="primary.TFrame")
        self.menu_frame.pack(side="left", fill="y")

        # Configuração do estilo para o menu cinza
        style = ttk.Style()
        style.configure("primary.TFrame", background="#333333")  # Cinza escuro

        # Botões do menu lateral
        self.botao_casa = ttk.Button(
            master=self.menu_frame,
            text="🏠 Home",
            bootstyle="secondary",
            command=self.mostrar_tela_inicial,
        )
        self.botao_casa.pack(fill="x", pady=10, padx=5)

        self.botao_duvidas = ttk.Button(
            master=self.menu_frame,
            text="❓ Dúvidas",
            bootstyle="secondary",
            command=self.mostrar_pergunta_frame,
        )
        self.botao_duvidas.pack(fill="x", pady=10, padx=5)

        versao = ttk.Label(
            master=self.menu_frame,
            text="v1.2",
            font=("Helvetica", 8),
        )
        versao.pack(side="bottom")

        self.botao_feedback = ttk.Button(
            master=self.menu_frame,
            text="Feedback",
            bootstyle="secondary",
        )
        self.botao_feedback.pack(fill="x", side="bottom", pady=10, padx=5)

        # Frames principais
        self.tela_inicial_frame = ttk.Frame(self)
        self.pergunta_frame = ttk.Frame(self)

        # Configuração da tela inicial e tela de dúvidas
        self.configurar_tela_inicial()
        self.configurar_pergunta_frame()

        # Inicialmente, exibe a tela inicial
        self.mostrar_tela_inicial()
        # icone
        icon = ttk.PhotoImage(file="icone.png")
        self.tk.call("wm", "iconphoto", self._w, icon)

    def configurar_tela_inicial(self):
        label_boas_vindas = ttk.Label(
            master=self.tela_inicial_frame,
            text="Bem-vindo ao Trainer",
            font=("Helvetica", 24),
        )
        label_boas_vindas.pack(pady=20)

        descricao = ttk.Label(
            master=self.tela_inicial_frame,
            text="Aqui você pode tirar dúvidas e interagir com nosso sistema.",
            font=("Helvetica", 14),
        )
        descricao.pack(pady=10)

    def configurar_pergunta_frame(self):
        # Configurar estilos personalizados
        self.configurar_estilos()

        # Campo de Pergunta
        label_pergunta = ttk.Label(
            master=self.pergunta_frame,
            text="Olá, Como posso ajudar?",
            font=("Helvetica", 16),
        )
        label_pergunta.pack(pady=(10, 10))

        self.entry_pergunta = ttk.Entry(master=self.pergunta_frame, width=50)
        self.entry_pergunta.pack(pady=(10, 10))

        # Botão de Perguntar
        botao_perguntar = ttk.Button(
            master=self.pergunta_frame,
            text="Perguntar",
            command=self.processar_pergunta,
            style="RoxoEscuro.TButton",  # Estilo personalizado
        )
        botao_perguntar.pack(pady=10)

        # Área para exibir a resposta
        self.resposta_frame = ttk.Frame(master=self.pergunta_frame)
        self.resposta_frame.pack(pady=20, padx=20, fill="both", expand=True)

    def configurar_estilos(self):
        # Configura estilos para botões personalizados
        style = ttk.Style()

        # Estilo inicial do botão
        style.configure(
            "RoxoEscuro.TButton",
            background="#6d00ff",  # Roxo
            foreground="white",
            font=("Helvetica", 12),
            borderwidth=0,  # Sem borda
        )

        # Adicionando um estilo especial para hover
        style.map(
            "RoxoEscuro.TButton",
            background=[("active", "#5000bc")],  # Roxo mais escuro no hover
        )

    def processar_pergunta(self):
        self.ocultar_resposta()
        pergunta = self.entry_pergunta.get().strip()
        if not pergunta:
            self.mostrar_resposta_texto("Por favor, digite uma pergunta.")
            return

        # Busca no banco de dados por tags relacionadas
        resposta = banco_de_dados.buscar_resposta(pergunta)
        if resposta:
            self.exibir_resposta(resposta)
        else:
            self.mostrar_cadastro_pergunta(pergunta)

    def exibir_resposta(self, resposta):
        tipo = resposta.get("tipo", "texto")
        if tipo == "texto":
            self.mostrar_resposta_texto(resposta.get("resposta"))
        elif tipo.startswith("imagem"):
            self.mostrar_resposta_com_imagem(
                resposta.get("resposta"), resposta.get("imagem")
            )
        elif tipo == "opcoes":
            self.mostrar_opcoes(resposta.get("opcoes", []))

    def mostrar_resposta_texto(self, resposta):
        self.ocultar_resposta()
        label_resposta = ttk.Label(
            master=self.resposta_frame, text=resposta, font=("Helvetica", 14)
        )
        label_resposta.pack(pady=10)

    def mostrar_resposta_com_imagem(self, texto, caminho_imagem):
        self.ocultar_resposta()
        if caminho_imagem:
            try:
                imagem = Image.open(caminho_imagem)
                imagem = imagem.resize(
                    (300, 300), Image.Resampling.LANCZOS
                )  # Redimensionar a imagem
                imagem_tk = ImageTk.PhotoImage(imagem)

                label_imagem = ttk.Label(master=self.resposta_frame, image=imagem_tk)
                label_imagem.image = (
                    imagem_tk  # Manter referência para evitar garbage collection
                )
                label_imagem.pack(pady=10)
            except Exception as e:
                self.mostrar_resposta_texto("Erro ao carregar a imagem: " + str(e))
        if texto:
            label_resposta = ttk.Label(
                master=self.resposta_frame, text=texto, font=("Helvetica", 14)
            )
            label_resposta.pack(pady=10)

    def mostrar_opcoes(self, opcoes):
        self.ocultar_resposta()
        for opcao in opcoes:
            botao_opcao = ttk.Button(
                master=self.resposta_frame,
                text=opcao.get("texto"),
                command=lambda o=opcao: self.mostrar_resposta_texto(o.get("resposta")),
                style="RoxoEscuro.TButton",  # Estilo personalizado aplicado
            )
            botao_opcao.pack(pady=5, padx=10)  # Adicionar padding para ajuste estético

    def mostrar_cadastro_pergunta(self, pergunta):
        self.ocultar_resposta()
        label_info = ttk.Label(
            master=self.resposta_frame,
            text="Dúvida não encontrada no nosso banco de dados. Deseja cadastrá-la?",
            font=("Helvetica", 14),
        )
        label_info.pack(pady=10)

        frame_botoes_sim_nao = ttk.Frame(self.resposta_frame)
        frame_botoes_sim_nao.pack(pady=10)

        # Botão "Sim"
        botao_sim = ttk.Button(
            master=frame_botoes_sim_nao,
            text="Sim",
            command=lambda: self.cadastrar_pergunta(
                pergunta
            ),  # Passando a pergunta para o método
            style="RoxoEscuro.TButton",
        )
        botao_sim.pack(side="left", padx=10)  # Alinha à esquerda dentro do frame

        # Botão "Não"
        botao_nao = ttk.Button(
            master=frame_botoes_sim_nao,
            text="Não",
            command=self.mostrar_resposta_nao_cadastrada,  # Chama o método para esconder os botões
            style="RoxoEscuro.TButton",
        )
        botao_nao.pack(side="left", padx=10)  # Ao lado do botão "Sim"

    def cadastrar_pergunta(self, pergunta):
        """Método que cadastra a pergunta no arquivo TXT na área de trabalho"""
        try:
            # Caminho para salvar o arquivo TXT na área de trabalho
            caminho_area_trabalho = os.path.join(
                os.path.expanduser("~"), "Desktop", "duvidas.txt"
            )

            # Salva a pergunta no arquivo
            with open(caminho_area_trabalho, "a", encoding="utf-8") as arquivo:
                arquivo.write(
                    pergunta + "\n"
                )  # Adiciona a pergunta no arquivo, cada uma em uma nova linha

            self.mostrar_resposta_texto("Dúvida cadastrada com sucesso!")
            self.ocultar_botoes_sim_nao()

        except Exception as e:
            self.mostrar_resposta_texto(f"Erro ao cadastrar a pergunta: {str(e)}")

    def mostrar_resposta_nao_cadastrada(self):
        """Método que exibe mensagem e oculta os botões Sim e Não"""
        self.mostrar_resposta_texto("Dúvida não cadastrada!")
        self.ocultar_botoes_sim_nao()

    def ocultar_botoes_sim_nao(self):
        """Método para ocultar os botões Sim e Não"""
        for widget in self.resposta_frame.winfo_children():
            if isinstance(widget, ttk.Button):
                widget.pack_forget()

    def ocultar_resposta(self):
        for widget in self.resposta_frame.winfo_children():
            widget.destroy()

    def mostrar_tela_inicial(self):
        self.pergunta_frame.pack_forget()
        self.tela_inicial_frame.pack(fill="both", expand=True)

    def mostrar_pergunta_frame(self):
        self.tela_inicial_frame.pack_forget()
        self.pergunta_frame.pack(fill="both", expand=True)


if __name__ == "__main__":
    app = SistemaAtendimentoApp()
    app.mainloop()
