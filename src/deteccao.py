
import cv2


def detectar_movimento(frame, detector, area_minima=1000):
    
    # Identifica os pixels que diferem do fundo
    mascara = detector.apply(frame)

    # Reduz ruídos e amplia as regiões detectadas
    mascara = cv2.medianBlur(mascara, 5)
    mascara = cv2.dilate(mascara, None, iterations=2)

    # Encontra os contornos do movimento
    contornos, _ = cv2.findContours(
        mascara, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    # Calcula os limites das três zonas
    largura = frame.shape[1]
    limite_zona1 = largura // 3
    limite_zona2 = (largura * 2) // 3

    zonas_ativas = set()

    for contorno in contornos:
        # Ignora movimentos muito pequenos
        if cv2.contourArea(contorno) < area_minima:
            continue

        # Calcula o retângulo do movimento
        x, y, w, h = cv2.boundingRect(contorno)

        # Desenha o retângulo verde
        cv2.rectangle(
            frame, (x, y), (x + w, y + h),
            (0, 255, 0), 2
        )

        # Identifica a zona pelo centro horizontal
        centro_x = x + w // 2

        if centro_x < limite_zona1:
            zona = 1
        elif centro_x < limite_zona2:
            zona = 2
        else:
            zona = 3

        zonas_ativas.add(zona)

    return zonas_ativas
