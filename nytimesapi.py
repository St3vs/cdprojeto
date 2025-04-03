import requests
import json
import logging
import os
from datetime import datetime

# Configuração do logging (apenas dia e hora)
logging.basicConfig(
    filename="logging.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M"
)

# Chave da API do NYT
API_KEY = "mtE9UItUjdAMkiAuOo0ljc9P60647UqL"
URL = f"https://api.nytimes.com/svc/topstories/v2/home.json?api-key={API_KEY}"

# Nome do arquivo JSON
JSON_FILE = "dados.json"


def obter_dados():
    """Obtém os dados da API do NYT e retorna uma lista de artigos"""
    try:
        response = requests.get(URL)
        response.raise_for_status() 
        data = response.json()

        if "results" not in data:
            logging.error("A chave 'results' não foi encontrada na resposta da API.")
            return []
        
        return data["results"]  # Lista de artigos
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


def guardar_json(data):
    """Guarda os dados no arquivo JSON"""
    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def atualizar_dados():
    """Obtém novos artigos e atualiza o JSON sem duplicar"""
    novos_dados = obter_dados()
    if not novos_dados:
        logging.warning("Nenhum dado novo encontrado.")
        return

    artigos_existentes = carregar_json()
    urls_existentes = {artigo.get("url", "") for artigo in artigos_existentes}  # Usando URL como identificador único

    novos_adicionados = 0
    for artigo in novos_dados:
        if "url" in artigo and artigo["url"] not in urls_existentes:
            artigos_existentes.append(artigo)  # Adiciona o artigo completo
            novos_adicionados += 1

    if novos_adicionados > 0:
        guardar_json(artigos_existentes)
        logging.info(f"Adicionados {novos_adicionados} artigos. Total: {len(artigos_existentes)}")
    else:
        logging.info("Nenhum novo artigo foi adicionado.")


# Executar o script
if __name__ == "__main__":
    atualizar_dados()


