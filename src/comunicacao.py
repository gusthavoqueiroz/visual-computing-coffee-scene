
import socket


def enviar_comando(zona):
    try:
        with socket.create_connection(
            ("127.0.0.1", 5050),
            timeout=0.1
        ) as conexao:
            mensagem = f"ZONA_{zona}"
            conexao.sendall(mensagem.encode("utf-8"))

    except OSError:
        # Mantém a webcam funcionando mesmo
        # quando o Blender não estiver aberto
        pass
