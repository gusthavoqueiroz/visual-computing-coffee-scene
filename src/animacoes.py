
import cv2
from pathlib import Path
import numpy as np


def carregar_animacoes():

    # Localiza a pasta principal do projeto
    pasta_projeto = Path(__file__).resolve().parent.parent

    # Define as pastas das três animações
    pastas = {
        1: pasta_projeto / "assets" / "zona1_cadeiras",
        2: pasta_projeto / "assets" / "zona2_pratos",
        3: pasta_projeto / "assets" / "zona3_copos_talheres"
    }

    # Dicionário para armazenar os frames
    animacoes = {}

    for zona, pasta in pastas.items():
        arquivos = sorted(pasta.glob("*.png"))
        frames = []

        for arquivo in arquivos:
            imagem = cv2.imread(str(arquivo), cv2.IMREAD_UNCHANGED)

            if imagem is not None:
                frames.append(imagem)

        animacoes[zona] = frames
        print(f"Zona {zona}: {len(frames)} frames carregados")

    return animacoes


def sobrepor_imagem(frame, imagem, x, y, tamanho=180):
    
    # Redimensiona a imagem
    imagem = cv2.resize(imagem, (tamanho, tamanho))

    # Obtém as dimensões
    altura_frame, largura_frame = frame.shape[:2]
    altura_img, largura_img = imagem.shape[:2]

    # Calcula a área visível
    x1 = max(x, 0)
    y1 = max(y, 0)
    x2 = min(x + largura_img, largura_frame)
    y2 = min(y + altura_img, altura_frame)

    # Verifica se a imagem está dentro da webcam
    if x1 >= x2 or y1 >= y2:
        return

    # Recorta a imagem PNG
    recorte = imagem[y1 - y:y2 - y, x1 - x:x2 - x]

    # Seleciona a região correspondente da webcam
    regiao = frame[y1:y2, x1:x2]

    # Calcula a transparência
    alfa = recorte[:, :, 3:4].astype(np.float32) / 255.0

    # Obtém os canais de cor
    cores = recorte[:, :, :3].astype(np.float32)

    # Mistura o PNG com a webcam
    resultado = cores * alfa + regiao.astype(np.float32) * (1 - alfa)

    # Atualiza a imagem da webcam
    frame[y1:y2, x1:x2] = resultado.astype(np.uint8)

