# OpenCV
import cv2

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
    
    # Aplica o detector de movimento
    mascara = detector.apply(frame)

    # Remove pequenos ruídos da imagem
    mascara = cv2.medianBlur(mascara, 5)

    # Amplia as regiões de movimento
    mascara = cv2.dilate(mascara, None, iterations=2)

    # Encontra os contornos
    contornos, _ = cv2.findContours(
        mascara, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    for contorno in contornos:
        # Ignora movimentos pequenos | Calcula a área geométrica do contorno
        if cv2.contourArea(contorno) < 1000:
            continue

        # Calcula o retângulo do movimento
        x, y, w, h = cv2.boundingRect(contorno)

        # Desenha o retângulo verde | frame, ponto superior esquerdo, ponto inferior direito, cor, espessura
        cv2.rectangle(
            frame, (x, y), (x + w, y + h),
            (0, 255, 0), 2
        )


        # Calcula o centro horizontal do movimento
        centro_x = x + w // 2

        # Obtém a largura da imagem | 1 = largura, 0 = altura
        largura_frame = frame.shape[1]

        # Calcula os limites das três zonas
        limite_zona1 = largura_frame // 3
        limite_zona2 = (largura_frame * 2) // 3

        # Identifica em qual zona aconteceu o movimento
        if centro_x < limite_zona1:
            zona = 1
        elif centro_x < limite_zona2:
            zona = 2
        else:
            zona = 3

        # Mostra a zona detectada na imagem
        cv2.putText(
            frame,
            f"Movimento: Zona {zona}",
            (x, max(y - 10, 20)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 0),
            2
        )

    
    # Obtém as dimensões da imagem | :2 se refere a altura e largura, ignorando o restante (canais de cor)
    altura, largura = frame.shape[:2]

    # Calcula a largura de cada zona
    largura_zona = largura // 3

    # Desenha duas linhas verticais
    cv2.line(frame, (largura_zona, 0), (largura_zona, altura), (255, 255, 255), 2)
    cv2.line(frame, (largura_zona * 2, 0), (largura_zona * 2, altura), (255, 255, 255), 2)


    # Identifica cada zona
    cv2.putText(frame, "ZONA 1 - CADEIRAS", (10, 30),
        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

    cv2.putText(frame, "ZONA 2 - PRATOS", (largura_zona + 10, 30),
        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

    cv2.putText(frame, "ZONA 3 - COPOS", (largura_zona * 2 + 10, 30),
        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)


    # Exibe a imagem com as três zonas
    cv2.imshow("Computacao Visual - Webcam", frame)

    # Pressione Q para encerrar
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


# Libera a webcam e fecha as janelas
camera.release()
cv2.destroyAllWindows()
