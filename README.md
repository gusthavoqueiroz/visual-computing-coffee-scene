# Projeto de Computação Visual

**Universidade:** Universidade do Algarve (UAlg)  
**Unidade Curricular:** Computação Visual  
**Autor:** Gusthavo Freitas Queiroz  


## 1. Descrição do projeto

Este projeto apresenta um sistema interativo de Computação Visual que integra modelação e animação 3D no Blender com deteção de movimento em tempo real utilizando Python e OpenCV.

O sistema utiliza uma webcam para identificar movimentos em três zonas verticais da imagem. Cada zona está associada a uma animação específica de objetos de uma esplanada virtual.

As animações são apresentadas sobre a imagem da webcam através de sequências PNG com transparência. Adicionalmente, os movimentos detetados são comunicados ao Blender através de uma ligação TCP local, permitindo controlar as animações dos objetos 3D.

## 2. Tecnologias utilizadas

- Python
- OpenCV
- Blender 5.2.2
- Blender Python API (`bpy`)
- Sockets TCP
- JSON
- Git e GitHub

## 3. Cena 3D

A cena foi desenvolvida no Blender e representa uma esplanada com mesa, cadeiras, pratos, copos e talheres.

Os objetos animados estão organizados em três coleções:

| Zona | Coleção | Objetos animados |
|---|---|---|
| 1 | `z1-cadeiras` | 4 |
| 2 | `z2-pratos` | 3 |
| 3 | `z3-copos-talheres` | 6 |

Cada animação possui 48 frames, com uma taxa de 24 FPS, correspondendo a aproximadamente dois segundos.

## 4. Deteção de movimento

A deteção de movimento é realizada utilizando o algoritmo MOG2 do OpenCV.

O processamento inclui:

1. Captura de imagens da webcam.
2. Espelhamento horizontal da imagem.
3. Subtração do fundo com MOG2.
4. Redução de ruídos com filtro de mediana.
5. Dilatação da máscara de movimento.
6. Identificação de contornos.
7. Filtragem de regiões com área inferior a 1000 pixels quadrados.
8. Cálculo de bounding boxes.
9. Identificação da zona correspondente ao centro horizontal de cada movimento.

## 5. Funcionamento das animações

Quando um movimento é identificado numa zona, o sistema inicia a animação PNG correspondente.

As animações são carregadas a partir de sequências de imagens RGBA e sobrepostas à imagem da webcam utilizando o canal alfa.

As três zonas possuem controlo independente, permitindo executar animações simultaneamente.

## 6. Comunicação com o Blender

A comunicação entre o programa OpenCV e o Blender é realizada através de sockets TCP.

O Blender executa um servidor local em `127.0.0.1`, na porta `5050`.

Os comandos utilizados são:

- `ZONA_1`: anima as cadeiras.
- `ZONA_2`: anima os pratos.
- `ZONA_3`: anima os copos e talheres.

O servidor utiliza uma thread para receber comandos e um temporizador da API do Blender para atualizar os objetos na thread principal.

As animações são controladas individualmente através das curvas de animação dos objetos.

## 7. Registo de eventos e evidências

Os movimentos identificados são registados num ficheiro JSON.

Cada evento contém:

- Zona ativada.
- Data e hora de início no formato ISO 8601.
- Duração do evento em segundos.
- Caminho da imagem de evidência.
- Bounding boxes identificados durante o movimento.

As imagens de evidência são guardadas em `registros/evidencias/`, enquanto os dados dos eventos são armazenados em `registros/eventos.json`.

O sistema utiliza uma tolerância de 0,5 segundo sem movimento para determinar o fim de um evento.

## 8. Organização do código

Os principais módulos são:

| Arquivo | Responsabilidade |
|---|---|
| `src/main.py` | Coordenação do sistema e webcam |
| `src/deteccao.py` | Deteção de movimento e bounding boxes |
| `src/animacoes.py` | Carregamento e sobreposição das animações |
| `src/visualizacao.py` | Representação visual das zonas |
| `src/comunicacao.py` | Envio de comandos TCP |
| `src/servidor_blender.py` | Servidor e controlo das animações no Blender |
| `src/registros.py` | Armazenamento dos eventos em JSON |

## 9. Execução do projeto

### Dependências

É necessário instalar Python, OpenCV e Blender 5.2.2, além de possuir uma webcam funcional.

Instalação do OpenCV:

```bash
pip install opencv-python
```

### Iniciar o Blender

1. Abrir o ficheiro da cena no Blender.
2. Abrir o script `servidor_blender.py` no editor de texto do Blender.
3. Executar o script para iniciar o servidor TCP.
4. Manter o Blender aberto.

### Iniciar o OpenCV

Na pasta principal do projeto, executar:

```bash
python src/main.py
```

O programa abrirá a webcam e identificará os movimentos nas três zonas.

Para encerrar a aplicação, pressionar `Q` na janela da webcam.

## 10. Utilização de Inteligência Artificial

Durante o desenvolvimento, foi utilizado o ChatGPT como ferramenta de apoio à programação e à compreensão de conceitos técnicos.

O apoio incluiu explicações sobre Python, OpenCV, API do Blender, organização modular, comunicação TCP, tratamento de erros e documentação.

O código foi integrado, executado e testado no ambiente de desenvolvimento do projeto, com acompanhamento e validação dos resultados pelo autor.

## 11. Conclusão

O projeto demonstra a integração entre visão computacional e animação 3D, permitindo que movimentos captados por uma webcam desencadeiem respostas visuais em tempo real.

A implementação combina deteção de movimento, processamento de imagem, animações com transparência, comunicação entre aplicações e registo estruturado de eventos.