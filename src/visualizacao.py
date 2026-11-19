import cv2


def desenhar_zonas(frame, zonas_ativas):
    
    # Obtém as dimensões da webcam
    altura, largura = frame.shape[:2]
    largura_zona = largura // 3

    # Desenha as linhas divisórias
    cv2.line(
        frame, (largura_zona, 0),
        (largura_zona, altura),
        (255, 255, 255), 2
    )

    cv2.line(
        frame, (largura_zona * 2, 0),
        (largura_zona * 2, altura),
        (255, 255, 255), 2
    )

    # Identifica as três zonas
    nomes = {
        1: "ZONA 1 - CADEIRAS",
        2: "ZONA 2 - PRATOS",
        3: "ZONA 3 - COPOS"
    }

    for zona, nome in nomes.items():
        posicao_x = (zona - 1) * largura_zona + 10

        cv2.putText(
            frame, nome, (posicao_x, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5, (255, 255, 255), 2
        )

    # Exibe as zonas que detectaram movimento
    for zona in sorted(zonas_ativas):
        cv2.putText(
            frame,
            f"Movimento: Zona {zona}",
            (10, 60 + (zona - 1) * 25),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6, (0, 255, 0), 2
        )
