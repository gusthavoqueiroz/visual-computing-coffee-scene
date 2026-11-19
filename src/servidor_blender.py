
import bpy
import socket
import threading
import queue
import time

# Configurações da comunicação
HOST = "127.0.0.1"
PORTA = 5050

# Configurações das animações
FPS = 24
TOTAL_FRAMES = 48

# Armazena os comandos recebidos
comandos = queue.Queue()

# Relaciona cada comando à coleção do Blender
COLECOES = {
    "ZONA_1": "z1-cadeiras",
    "ZONA_2": "z2-pratos",
    "ZONA_3": "z3-copos-talheres"
}

# Controla o início de cada animação
inicios = {
    zona: None for zona in COLECOES
}

# Armazena os objetos animados de cada coleção
objetos = {}

for zona, nome_colecao in COLECOES.items():
    colecao = bpy.data.collections.get(nome_colecao)
    objetos[zona] = []

    if colecao is None:
        print(f"Coleção não encontrada: {nome_colecao}")
        continue

    for obj in colecao.all_objects:
        if obj.animation_data and obj.animation_data.action:
            objetos[zona].append(obj)

    print(f"{zona}: {len(objetos[zona])} objetos animados")


def receber_comandos():
    # Cria o servidor TCP local
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor:
            servidor.setsockopt(
                socket.SOL_SOCKET,
                socket.SO_REUSEADDR,
                1
            )

            servidor.bind((HOST, PORTA))
            servidor.listen()

            print(f"Servidor Blender iniciado na porta {PORTA}")

            while True:
                conexao, _ = servidor.accept()

                with conexao:
                    dados = conexao.recv(1024)

                    if dados:
                        mensagem = dados.decode("utf-8").strip()
                        comandos.put(mensagem)

    except OSError as erro:
        print(f"Erro no servidor TCP: {erro}")


def aplicar_animacao(obj, frame_animacao):
    # Obtém a Action e o slot do objeto
    animacao = obj.animation_data

    if animacao is None:
        return

    action = animacao.action
    slot = animacao.action_slot

    if action is None or slot is None:
        return

    # Percorre as camadas da Action no Blender 5.2
    for camada in action.layers:
        for faixa in camada.strips:
            canal = faixa.channelbag(slot)

            if canal is None:
                continue

            # Avalia os keyframes no instante desejado
            for fc in canal.fcurves:
                valor = fc.evaluate(frame_animacao)

                if fc.data_path == "location":
                    obj.location[fc.array_index] = valor

                elif fc.data_path == "rotation_euler":
                    obj.rotation_euler[fc.array_index] = valor

                elif fc.data_path == "scale":
                    obj.scale[fc.array_index] = valor


def atualizar_animacoes():
    agora = time.monotonic()

    # Processa os comandos recebidos
    while not comandos.empty():
        zona = comandos.get()

        if zona not in COLECOES:
            print(f"Comando desconhecido: {zona}")
            continue

        # Inicia apenas se a zona não estiver animando
        if inicios[zona] is None:
            inicios[zona] = agora
            print(f"Iniciando animação: {zona}")

    # Atualiza cada zona separadamente
    for zona, inicio in inicios.items():
        if inicio is None:
            continue

        tempo_decorrido = agora - inicio

        # Converte o tempo decorrido para frames
        frame_animacao = 1 + int(tempo_decorrido * FPS)

        # Limita a animação aos 48 frames
        if frame_animacao >= TOTAL_FRAMES:
            frame_animacao = TOTAL_FRAMES
            inicios[zona] = None
            print(f"Animação finalizada: {zona}")

        # Atualiza somente os objetos da zona ativa
        for obj in objetos[zona]:
            aplicar_animacao(obj, frame_animacao)

    # Atualiza aproximadamente 24 vezes por segundo
    return 1.0 / FPS


# Inicia a comunicação sem bloquear o Blender
thread = threading.Thread(
    target=receber_comandos,
    daemon=True
)
thread.start()

# Executa a atualização na thread principal
bpy.app.timers.register(atualizar_animacoes)

print("Controle independente das três zonas iniciado!")
