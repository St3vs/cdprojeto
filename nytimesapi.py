import requests
import json
import logging
import os
from datetime import datetime

# Configuração do logging para registrar apenas o dia e hora
logging.basicConfig(
    filename="scraper.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M"  # Formato de data e hora (ano-mês-dia hora:minuto)
)

# Chave da API do NYT
API_KEY = "mtE9UItUjdAMkiAuOo0ljc9P60647UqL"
URL = f"https://api.nytimes.com/svc/news/v3/content/all/all.json?api-key={API_KEY}"

# Nome do arquivo JSON para armazenar os artigos
JSON_FILE = "nyt_articles.json"

def obter_dados():
    """Obtém os dados da API do NYT e retorna uma lista de artigos"""
    try:
        response = requests.get(URL)
        response.raise_for_status()  # Lança erro se a resposta for ruim (ex: 404, 500)
        data = response.json()

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
                logging.error("Erro ao carregar o JSON, arquivo pode estar corrompido.")
                return []
    return []

def salvar_json(data):
    """Salva os dados no arquivo JSON"""
    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def atualizar_dados():
    """Obtém novos artigos e atualiza o JSON sem duplicar"""
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

    # Log usando o horário padrão do sistema, apenas com dia e hora
    agora = datetime.now().strftime("%Y-%m-%d %H:%M")  # Somente dia e hora
    logging.info(f"{agora} - Adicionados {novos_adicionados} artigos. Total: {len(artigos_existentes)}")

# Executar o script
if __name__ == "__main__":
    atualizar_dados()
