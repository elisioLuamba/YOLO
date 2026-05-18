Para configurar o YOLOv8 (ou v11) em um ambiente Conda, o processo precisa ser limpo e isolado para evitar conflitos de bibliotecas de visão computacional. Como você está em Luanda, recomendo garantir que a conexão esteja estável durante o download dos pesos do modelo.

Aqui está o passo a passo direto para criar o ambiente e inicializar o projeto:

1. Criação e Preparação do Ambiente
Abra o seu terminal (ou Anaconda Prompt) e execute os seguintes comandos:

Bash
# 1. Criar o ambiente com Python 3.10 (estável para IA)
conda create -n vision_ergonomia python=3.10 -y

# 2. Ativar o ambiente
conda activate vision_ergonomia

# 3. Instalar o PyTorch (Essencial para o YOLO)
# Se tiver GPU NVIDIA, use o comando com suporte a CUDA. Se não, use CPU:
conda install pytorch torchvision torchaudio cpuonly -c pytorch -y
2. Instalação do YOLO (Ultralytics)
A biblioteca ultralytics já contém tudo o que você precisa: o modelo, os scripts de treinamento e as ferramentas de predição de pose.

Bash
# Instalar a biblioteca principal
pip install ultralytics

# Instalar dependências extras para manipulação de vídeo e interface
pip install opencv-python matplotlib streamlit
3. Inicialização e Teste de Pose (Tempo Real)
Para o seu sistema de ergonomia, você não usará o YOLO comum, mas o YOLO-Pose. Vamos criar um script rápido (main.py) para testar se a câmera está detectando o corpo humano corretamente.

Script de Inicialização Rápida:
Python
from ultralytics import YOLO
import cv2

# Carrega o modelo nano de pose (mais leve para tempo real)
model = YOLO('yolov8n-pose.pt')

# Inicia a captura da webcam
cap = cv2.VideoCapture(0)

while cap.isOpened():
    success, frame = cap.read()
    if success:
        # Executa a detecção de esqueleto
        results = model(frame, stream=True)

        for r in results:
            # Desenha os pontos e conexões no frame
            annotated_frame = r.plot()
            
        cv2.imshow("Teste de Ergonomia - YOLOv8", annotated_frame)
        
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

cap.release()
cv2.destroyAllWindows()
4. Estrutura do Projeto para o TCC
Para organizar a sua simulação, recomendo esta estrutura de pastas:

/models: Onde ficarão os arquivos .pt (pesos do YOLO).

/src: Scripts de cálculo ergonômico (ângulos, NR-17).

/app: O código do seu aplicativo para o supervisor (Streamlit).

/videos: Vídeos da obra para simular o "tempo real" sem precisar de uma câmera ao vivo o tempo todo.

Dica de Performance para a Simulação
Como o foco é o Supervisor, você pode rodar o processamento do YOLO em um script separado e enviar apenas os alertas para o aplicativo. Isso garante que a interface do supervisor não trave enquanto a IA processa o vídeo.

Nota: Se o seu computador não tiver uma placa de vídeo dedicada (GPU), certifique-se de usar sempre os modelos marcados com "n" (ex: yolov8n-pose.pt), pois são otimizados para rodar em CPUs comuns com baixa latência.


conda remove --name vision_ergonomia --all -y