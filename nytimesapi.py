import requests
import json
import logging
import os
import time
from datetime import datetime
import schedule

# Configuração do logging para registar apenas o dia e hora
logging.basicConfig(
    filename="logging.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M"  # Formato de data e hora (ano-mês-dia hora:minuto)
)

# Chave da API do NYT
API_KEY = "mtE9UItUjdAMkiAuOo0ljc9P60647UqL"
URL = f"https://api.nytimes.com/svc/news/v3/content/section/front.json?api-key={API_KEY}"

# Nome do arquivo JSON para armazenar os artigos
JSON_FILE = "dados.json"

def obter_dados():
    """Obtém os dados da página inicial do NYT e retorna uma lista de artigos"""
    try:
        response = requests.get(URL)
        response.raise_for_status()
        data = response.json()

        # Extrai os artigos da resposta
        return data.get("results", [])  # Retorna lista vazia se "results" não existir
    except requests.exceptions.RequestException as e:
        logging.error(f"Erro na requisição à API: {e}")
        return []

def carregar_json():
    """Carrega os dados já armazenados no JSON"""
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                logging.error("Erro ao carregar o JSON.")
                return []
    return []

def salvar_json(data):
    """Guarda os dados no arquivo JSON"""
    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def atualizar_dados():
    """Obtém os novos artigos da página inicial e atualiza o JSON sem duplicar"""
    novos_dados = obter_dados()
    if not novos_dados:
        logging.warning("Nenhum dado novo encontrado.")
        return

    artigos_existentes = carregar_json()
    titulos_existentes = {artigo.get("title", "") for artigo in artigos_existentes}

    novos_adicionados = 0
    for artigo in novos_dados:
        # Verifica se as chaves essenciais existem antes de adicionar
        if "title" in artigo and "url" in artigo and "published_date" in artigo:
            if artigo["title"] not in titulos_existentes:
                artigos_existentes.append({
                    "title": artigo["title"],
                    "url": artigo["url"],
                    "published_date": artigo["published_date"]
                })
                novos_adicionados += 1

    salvar_json(artigos_existentes)

    # Log atrvés do horário padrão do sistema, apenas com dia e hora
    agora = datetime.now().strftime("%Y-%m-%d %H:%M") 
    logging.info(f"{agora} - Adicionados {novos_adicionados} artigos. Total: {len(artigos_existentes)}")

# Executar o script
if __name__ == "__main__":
    atualizar_dados()

