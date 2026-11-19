# OpenCV
import cv2

# Controlar a velocidade da animação independentemente da velocidade da webcam
import time

from animacoes import carregar_animacoes, sobrepor_imagem
from deteccao import detectar_movimento
from visualizacao import desenhar_zonas


# Carrega as animações do Blender
animacoes = carregar_animacoes()


# Guarda o instante de início de cada animação
inicio_animacoes = {
    1: None,  # Cadeiras
    2: None,  # Pratos
    3: None   # Copos e talheres
}

# Velocidade das animações
FPS_ANIMACAO = 24


# Abre a webcam principal do computador - 0 a primeira webcam, 1 a segunda, e assim por diante
camera = cv2.VideoCapture(0)

# Verifica se a webcam foi aberta corretamente
if not camera.isOpened():
    print("Erro: não foi possível abrir a webcam.")
    exit()


# Cria o detector de movimento MOG2
detector = cv2.createBackgroundSubtractorMOG2(
    history=500,
    varThreshold=40,
    detectShadows=False
)


# Mantém a webcam funcionando
while True:
    # Captura uma imagem da webcam (bool, matriz de pixels - img)
    sucesso, frame = camera.read()

    if not sucesso:
        print("Erro ao capturar imagem.")
        break

    # Espelha a imagem horizontalmente
    frame = cv2.flip(frame, 1)

    # Obtém a altura e a largura da imagem
    altura, largura = frame.shape[:2]

    # Divide a webcam em três zonas
    largura_zona = largura // 3

    # Detecta os movimentos e retorna as zonas ativas
    zonas_ativas = detectar_movimento(frame, detector)

    
    # Controla as animações das três zonas
    for zona in (1, 2, 3):

        # Inicia a animação quando há movimento na zona
        if zona in zonas_ativas and inicio_animacoes[zona] is None:
            inicio_animacoes[zona] = time.monotonic()

        # Verifica se existe uma animação em execução
        if inicio_animacoes[zona] is not None and animacoes[zona]:

            # Calcula o tempo desde o início
            tempo_decorrido = time.monotonic() - inicio_animacoes[zona]

            # Calcula a duração de um ciclo completo
            duracao = len(animacoes[zona]) / FPS_ANIMACAO

            # Calcula o índice do frame atual
            indice_frame = int(tempo_decorrido * FPS_ANIMACAO) % len(animacoes[zona])

            # Define a posição da animação conforme a zona
            posicao_x = (zona - 1) * largura_zona + 30
            posicao_y = 150

            # Exibe o frame da animação
            sobrepor_imagem(
                frame,
                animacoes[zona][indice_frame],
                posicao_x,
                posicao_y
            )

        # Encerra a animação após um ciclo
            if tempo_decorrido >= duracao:
                inicio_animacoes[zona] = None


    # Desenha as divisões e os textos das três zonas
    desenhar_zonas(frame, zonas_ativas)

    # Exibe a imagem com as três zonas
    cv2.imshow("Computacao Visual - Webcam", frame)


    # Pressione Q para encerrar
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


# Libera a webcam e fecha as janelas
camera.release()
cv2.destroyAllWindows()
