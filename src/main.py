
import cv2
import time
from datetime import datetime
from pathlib import Path

from animacoes import carregar_animacoes, sobrepor_imagem
from deteccao import detectar_movimento
from visualizacao import desenhar_zonas
from comunicacao import enviar_comando
from registros import salvar_evento


# Configurações
FPS_ANIMACAO = 24
TEMPO_TOLERANCIA = 0.5

PASTA_PROJETO = Path(__file__).resolve().parent.parent
PASTA_EVIDENCIAS = PASTA_PROJETO / "registros" / "evidencias"
PASTA_EVIDENCIAS.mkdir(parents=True, exist_ok=True)

# Carrega as animações
animacoes = carregar_animacoes()

inicio_animacoes = {
    1: None,
    2: None,
    3: None
}

# Controla os eventos de movimento
eventos_ativos = {
    1: None,
    2: None,
    3: None
}

# Inicia a webcam
camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("Erro ao abrir a webcam.")
    raise SystemExit

detector = cv2.createBackgroundSubtractorMOG2(
    history=500,
    varThreshold=40,
    detectShadows=False
)


def finalizar_evento(zona, evento):
    duracao = time.monotonic() - evento["inicio_monotonic"]

    salvar_evento(
        zona=zona,
        inicio=evento["inicio"],
        duracao=duracao,
        evidencia=evento["evidencia"],
        bounding_boxes=evento["bounding_boxes"]
    )

    print(f"[ZONA {zona}] Evento finalizado: {duracao:.2f}s")


try:
    while True:
        sucesso, frame = camera.read()

        if not sucesso:
            break

        frame = cv2.flip(frame, 1)

        altura, largura = frame.shape[:2]
        largura_zona = largura // 3

        # Detecta movimentos e suas coordenadas
        zonas_ativas, bounding_boxes = detectar_movimento(
            frame, detector
        )

        agora = time.monotonic()

        for zona in (1, 2, 3):

            # Início de um novo evento
            if zona in zonas_ativas:

                if eventos_ativos[zona] is None:
                    inicio = datetime.now().astimezone()

                    nome_evidencia = (
                        f"zona{zona}_"
                        f"{inicio.strftime('%Y%m%d_%H%M%S_%f')}.png"
                    )

                    caminho_evidencia = (
                        PASTA_EVIDENCIAS / nome_evidencia
                    )

                    # Salva uma imagem com o movimento detectado
                    cv2.imwrite(str(caminho_evidencia), frame)

                    eventos_ativos[zona] = {
                        "inicio": inicio,
                        "inicio_monotonic": agora,
                        "ultimo_movimento": agora,
                        "evidencia": str(
                            Path("evidencias") / nome_evidencia
                        ),
                        "bounding_boxes": bounding_boxes[zona].copy()
                    }

                    print(f"[ZONA {zona}] Movimento iniciado")

                else:
                    evento = eventos_ativos[zona]
                    evento["ultimo_movimento"] = agora

                    # Guarda os retângulos detectados
                    evento["bounding_boxes"].extend(
                        bounding_boxes[zona]
                    )

            # Finaliza quando não há movimento por 0,5 segundo
            elif eventos_ativos[zona] is not None:

                evento = eventos_ativos[zona]

                if agora - evento["ultimo_movimento"] >= TEMPO_TOLERANCIA:
                    finalizar_evento(zona, evento)
                    eventos_ativos[zona] = None

            # Inicia a animação PNG e a animação no Blender
            if zona in zonas_ativas and inicio_animacoes[zona] is None:
                inicio_animacoes[zona] = agora
                enviar_comando(zona)

            # Exibe a animação PNG
            if inicio_animacoes[zona] is not None and animacoes[zona]:

                tempo_decorrido = (
                    time.monotonic() - inicio_animacoes[zona]
                )

                duracao_animacao = (
                    len(animacoes[zona]) / FPS_ANIMACAO
                )

                if tempo_decorrido >= duracao_animacao:
                    inicio_animacoes[zona] = None

                else:
                    indice_frame = int(
                        tempo_decorrido * FPS_ANIMACAO
                    )

                    posicao_x = (
                        (zona - 1) * largura_zona + 30
                    )
                    posicao_y = 150

                    sobrepor_imagem(
                        frame,
                        animacoes[zona][indice_frame],
                        posicao_x,
                        posicao_y
                    )

        desenhar_zonas(frame, zonas_ativas)

        cv2.imshow("Computacao Visual - Webcam", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

finally:
    # Registra eventos que ainda estavam ativos
    for zona, evento in eventos_ativos.items():
        if evento is not None:
            finalizar_evento(zona, evento)

    camera.release()
    cv2.destroyAllWindows()
