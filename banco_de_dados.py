import json
import os
from difflib import SequenceMatcher

# Caminho para o arquivo de dados JSON
def carregar_dados():
    """Carrega o arquivo JSON contendo as perguntas e respostas."""
    caminho_arquivo = os.path.join(os.path.dirname(__file__), "respostas.json")

    try:
        with open(caminho_arquivo, "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)
        return dados
    except FileNotFoundError:
        return {"perguntas": {}}
    except json.JSONDecodeError as e:
        print(f"Erro ao carregar o arquivo JSON: {e}")
        return {"perguntas": {}}

def salvar_dados(dados):
    """Salva as alterações no arquivo JSON."""
    caminho_arquivo = os.path.join(os.path.dirname(__file__), "respostas.json")

    try:
        with open(caminho_arquivo, "w", encoding="utf-8") as arquivo:
            json.dump(dados, arquivo, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Erro ao salvar o arquivo JSON: {e}")
        return False

def calcular_similaridade(a, b):
    """Calcula a similaridade entre duas strings."""
    return SequenceMatcher(None, a, b).ratio()

def buscar_resposta(pergunta):
    """Busca uma resposta com base na pergunta fornecida."""
    dados = carregar_dados()
    pergunta = pergunta.lower()
    melhores_resultados = []

    for key, valor in dados["perguntas"].items():
        # Verificar tags diretamente relacionadas
        if any(tag in pergunta for tag in valor["tags"]):
            return valor  # Correspondência exata

        # Calcular similaridade com cada tag
        for tag in valor["tags"]:
            similaridade = calcular_similaridade(pergunta, tag)
            if similaridade > 0.6:  # Ajuste o limite conforme necessário
                melhores_resultados.append((similaridade, valor))

    # Ordenar os melhores resultados por similaridade
    if melhores_resultados:
        melhores_resultados.sort(key=lambda x: x[0], reverse=True)
        return melhores_resultados[0][1]

    return None

def cadastrar_duvida(pergunta):
    """
    Cadastra uma nova dúvida no arquivo JSON.
    A pergunta é salva com uma resposta padrão e nenhuma tag.
    """
    dados = carregar_dados()
    pergunta_lower = pergunta.lower()

    if pergunta_lower not in dados["perguntas"]:
        dados["perguntas"][pergunta_lower] = {
            "resposta": "Resposta não cadastrada.",
            "tags": []
        }
        sucesso = salvar_dados(dados)
        return sucesso
    return False
