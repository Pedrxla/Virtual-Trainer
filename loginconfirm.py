import json
import subprocess
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

# Função para carregar os dados de login
def load_user_data():
    with open("usuarios-e-senhas.json", "r") as file:
        return json.load(file)

# Função para verificar login
def check_login():
    username = username_entry.get()
    password = password_entry.get()
    users = load_user_data()

    if username in users and users[username]["senha"] == password:
        nome_usuario = users[username]["nome"]
        status_label.config(text=f"Olá, {nome_usuario}! Que bom ter você de volta.", foreground="white", font=("helvetica", 14))
        # Aguarda 1 segundo e então chama a função para abrir a nova página
        login.after(3000, open_main_page, "sistema_atendimento.py")
    else:
        status_label.config(text="Usuário ou senha incorretos!", foreground="red", font=("Helvetica", 12))

# Função para abrir a nova página após login bem-sucedido e rodar outro script
def open_main_page(script_path):
    # Fecha a janela de login atual
    login.destroy()
    # Executa outro script Python
    subprocess.Popen(["python", script_path])

# Função para mostrar mensagem de recuperação de senha
def mostrar_recuperacao_senha():
    label_recuperacao_de_senha = ttk.Label(
        login,
        text="Para recuperar sua senha envie um email com o título: recuperar senha para pedro@grupolima.net.br",
        font=("Helvetica", 14),
    )
    label_recuperacao_de_senha.pack(pady=10)

# Função para configurar os estilos
def configurar_estilos():
    style1 = ttk.Style()
    # tyle para botão login 
    style1.configure(
        "StyleLogin.TButton",
        background="#6c00ff",  # Roxo
        foreground="white",
        font=("Helvetica", 12),
        borderwidth=0,  # Sem borda
        
    )

    # Estilo para hover (efeito de fundo roxo mais escuro quando o botão é pressionado)
    style1.map(
        "StyleLogin.TButton",
        background=[("active", "#5000bc")],  # Roxo mais escuro no hover
    )
    
    
    #Style para botão esqueci senha
    
    style2 = ttk.Style()
    style2.configure(
        "StyleEsqueciSenha.TButton",
        background="#222222",  # Roxo
        foreground="#6c00ff",
        font=("Helvetica", 12),
        borderwidth=0,  # Sem borda
         
    )
    style2.map(
        "StyleEsqueciSenha.TButton",
        background=[("active", "#222222")],  # Roxo mais escuro no hover
        foreground=[("active", "#5000bc")]
    )
    
# Criação da aplicação (página de login)
login = ttk.Window(themename="darkly")
login.title("Página de Login")
login.geometry("1280x720")
login.resizable(True, True)

# Definir o ícone da janela
icon = ttk.PhotoImage(file="icone.png")
login.tk.call('wm', 'iconphoto', login._w, icon)

# Configurar estilos dos botões
configurar_estilos()

# Mensagem de boas vindas
label_boasvindas = ttk.Label(
    login, text="Olá, seja bem-vindo ao TrainerGL!", font=("Helvetica", 14)
)
label_boasvindas.pack(pady=20)

# Criação dos widgets
username_label = ttk.Label(login, text="Usuário:", font=("helvetica", 14))
username_label.pack(pady=5)

username_entry = ttk.Entry(login)
username_entry.pack(pady=5)

password_label = ttk.Label(login, text="Senha:", font=("helvetica", 14))
password_label.pack(pady=5)

password_entry = ttk.Entry(login, show="*")
password_entry.pack(pady=5)

# Botão de login
login_button = ttk.Button(
    login, text="Login", command=check_login, style="StyleLogin.TButton"
)
login_button.pack(pady=10)

# Botão "Esqueci minha senha"
esqueci_senha_button = ttk.Button(
    login,
    text="Esqueci minha senha",
    command=mostrar_recuperacao_senha,
    style="StyleEsqueciSenha.TButton",
)
esqueci_senha_button.pack(pady=10)

# Label de status
status_label = ttk.Label(login, text="")
status_label.pack(pady=5)

# Iniciar a aplicação (página de login)
login.mainloop()
