
import json
from datetime import datetime
from pathlib import Path


# Localiza a pasta principal do projeto
PASTA_PROJETO = Path(__file__).resolve().parent.parent

# Define onde os registros serão armazenados
PASTA_REGISTROS = PASTA_PROJETO / "registros"
PASTA_REGISTROS.mkdir(parents=True, exist_ok=True)

ARQUIVO_JSON = PASTA_REGISTROS / "eventos.json"


def salvar_evento(zona, inicio, duracao, evidencia, bounding_boxes):
    # Organiza os dados de um evento
    evento = {
        "zona": zona,
        "inicio": inicio.isoformat(timespec="seconds"),
        "duracao_segundos": round(duracao, 2),
        "evidencia": evidencia,
        "bounding_boxes": bounding_boxes
    }

    # Recupera os eventos anteriores
    eventos = []

    if ARQUIVO_JSON.exists():
        try:
            with open(ARQUIVO_JSON, "r", encoding="utf-8") as arquivo:
                eventos = json.load(arquivo)
        except (json.JSONDecodeError, OSError):
            eventos = []

    # Adiciona o novo evento
    eventos.append(evento)

    # Salva todos os eventos no arquivo JSON
    with open(ARQUIVO_JSON, "w", encoding="utf-8") as arquivo:
        json.dump(eventos, arquivo, indent=4, ensure_ascii=False)

    print(f"Evento registrado: Zona {zona}")
