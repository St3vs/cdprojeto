import requests
import json
import logging
import os
from datetime import datetime

# Configuração do logging
logging.basicConfig(filename="scraper.log", level=logging.INFO, format="%(asctime)s - %(message)s")

# Chave de API do NYT
API_KEY = "SUA_CHAVE_AQUI"
URL = "https://api.nytimes.com/svc/topstories/v2/world.json?api-key=" + API_KEY

# Nome do arquivo JSON
JSON_FILE = "nyt_articles.json"

def obter_dados():
    """Obtém os dados da API do NYT"""
    try:
        response = requests.get(URL)
        data = response.json()
        return data["results"]
    except Exception as e:
        logging.error(f"Erro ao obter dados: {e}")
        return []

def carregar_json():
    """Carrega os dados já armazenados"""
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def salvar_json(data):
    """Salva os dados em um arquivo JSON"""
    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def atualizar_dados():
    """Atualiza o JSON sem duplicar os artigos"""
    novos_dados = obter_dados()
    if not novos_dados:
        logging.warning("Nenhum dado novo encontrado.")
        return

    artigos_existentes = carregar_json()
    titulos_existentes = {artigo["title"] for artigo in artigos_existentes}

    novos_adicionados = 0
    for artigo in novos_dados:
        if artigo["title"] not in titulos_existentes:
            artigos_existentes.append({
                "title": artigo["title"],
                "url": artigo["url"],
                "published_date": artigo["published_date"]
            })
            novos_adicionados += 1

    salvar_json(artigos_existentes)
    logging.info(f"Adicionados {novos_adicionados} artigos. Total: {len(artigos_existentes)}")

# Executar o script
if __name__ == "__main__":
    atualizar_dados()
