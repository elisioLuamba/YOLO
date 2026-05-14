# Configuração do YOLOv8 / YOLOv11 com Conda para Sistema de Ergonomia

> Estrutura organizada para projeto de visão computacional aplicado à ergonomia e monitoramento corporal.

---

# 1. Criação e Preparação do Ambiente

Abra o terminal ou o **Anaconda Prompt** e execute os comandos abaixo.

## Criar o ambiente Conda

```bash
# Criar ambiente com Python 3.10
conda create -n vision_ergonomia python=3.10 -y
```

## Ativar o ambiente

```bash
conda activate vision_ergonomia
```

## Instalar PyTorch

### CPU (sem GPU NVIDIA)

```bash
conda install pytorch torchvision torchaudio cpuonly -c pytorch -y
```

### GPU NVIDIA (CUDA)

```bash
conda install pytorch torchvision torchaudio pytorch-cuda=12.1 -c pytorch -c nvidia -y
```

> Use a versão CUDA apenas se tiver GPU NVIDIA compatível.

---

# 2. Instalação do YOLO (Ultralytics)

A biblioteca `ultralytics` já inclui:

- YOLO Detection
- YOLO Pose
- Treinamento
- Inferência
- Exportação de modelos

## Instalar bibliotecas principais

```bash
pip install ultralytics
```

## Dependências adicionais

```bash
pip install opencv-python matplotlib streamlit
```

---

# 3. Teste Inicial do YOLO Pose em Tempo Real

Para o sistema de ergonomia, o modelo recomendado é o **YOLO Pose**, responsável por detectar:

- Cabeça
- Ombros
- Cotovelos
- Joelhos
- Posições articulares

---

# 4. Script Inicial (`main.py`)

Crie um arquivo chamado:

```text
main.py
```

E adicione o código abaixo:

```python
from ultralytics import YOLO
import cv2

# Carrega o modelo leve de pose
model = YOLO("yolov8n-pose.pt")

# Inicializa webcam
cap = cv2.VideoCapture(0)

while cap.isOpened():

    success, frame = cap.read()

    if success:

        # Executa detecção
        results = model(frame, stream=True)

        for r in results:

            # Frame anotado
            annotated_frame = r.plot()

        cv2.imshow(
            "Teste de Ergonomia - YOLOv8",
            annotated_frame
        )

        # Pressione Q para sair
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

cap.release()
cv2.destroyAllWindows()
```

---

# 5. Executar o Projeto

No terminal:

```bash
python main.py
```

Se tudo estiver correto:

- A webcam abrirá
- O YOLO baixará automaticamente os pesos
- O esqueleto corporal aparecerá na tela

---

# 6. Estrutura Recomendada do Projeto (TCC)

```text
vision_ergonomia/
│
├── models/
│   └── yolov8n-pose.pt
│
├── src/
│   ├── ergonomia.py
│   ├── angulos.py
│   └── postura.py
│
├── app/
│   └── dashboard.py
│
├── videos/
│   └── simulacao_obra.mp4
│
├── main.py
│
└── requirements.txt
```

---

# 7. Função de Cada Pasta

| Pasta | Objetivo |
|---|---|
| `models/` | Armazenar modelos `.pt` |
| `src/` | Lógica de ergonomia e cálculos |
| `app/` | Interface para supervisor |
| `videos/` | Simulações gravadas |
| `main.py` | Execução principal |

---

# 8. Melhor Posição da Câmera

## Vista lateral

A câmera lateral é a mais eficiente para:

- Detectar inclinação da coluna
- Flexão de joelhos
- Levantamento incorreto de carga
- Ângulo lombar

---

# 9. Problema da Caixa Tapar o Corpo

Quando a caixa cobre partes do corpo:

- Joelhos podem desaparecer
- Punhos podem sumir
- Quadril pode ficar parcialmente oculto

O YOLO Pose consegue estimar parcialmente posições corporais usando contexto corporal.

---

# 10. Estratégias para Melhorar a Detecção

## Opção 1: Câmera lateral elevada

Melhora visibilidade das pernas e coluna.

## Opção 2: Duas câmeras

- Lateral
- Frontal

Mais preciso, porém mais complexo.

## Opção 3: Vídeos simulados

Ideal para TCC.

Você controla:

- iluminação
- ângulo
- postura
- cenários

---

# 11. Detecção de Capacete e Óculos

Você pode combinar:

- YOLO Pose
- YOLO Detection

## Objetos detectáveis

| Objeto | Possível |
|---|---|
| Capacete | Sim |
| Óculos de proteção | Sim |
| Colete | Sim |
| Luvas | Sim |
| Máscara | Sim |

---

# 12. Exemplo de Lógica de Alertas

```python
if angulo_coluna > 45:
    alerta = "RISCO ERGONÔMICO"
```

```python
if sem_capacete:
    alerta = "EPI AUSENTE"
```

---

# 13. Modelos Recomendados

| Modelo | Uso |
|---|---|
| `yolov8n-pose.pt` | CPU fraca |
| `yolov8s-pose.pt` | Médio desempenho |
| `yolo11n-pose.pt` | YOLO v11 leve |
| `yolo11s-pose.pt` | Melhor precisão |

---

# 14. Dica de Performance

Separar:

## Processo 1

YOLO processa vídeo.

## Processo 2

Dashboard recebe alertas.

Isso evita:

- travamentos
- perda de FPS
- interface congelada

---

# 15. Dashboard com Streamlit

Executar:

```bash
streamlit run app/dashboard.py
```

O dashboard pode mostrar:

- status do trabalhador
- fadiga
- postura incorreta
- ausência de EPI
- alertas em tempo real

---

# 16. Ideias Fortes para o TCC

## Possíveis funcionalidades

- Monitoramento NR-17
- Índice de fadiga
- Contagem de movimentos repetitivos
- Tempo em postura inadequada
- Heatmap corporal
- Histórico do trabalhador
- Geração automática de relatórios

---

# 17. Pesquisas Recomendadas

```text
YOLOv8 Pose Estimation Ergonomics
```

```text
Construction Worker Pose Detection
```

```text
Human Pose Estimation Workplace Safety
```

```text
PPE Detection YOLOv8
```

```text
Ergonomic Risk Assessment Computer Vision
```

---

# 18. Resumo Técnico

```text
Visão Computacional
+ Inteligência Artificial
+ Biomecânica
+ Segurança do Trabalho
+ Monitoramento em Tempo Real
```

Esse projeto possui potencial para:

- TCC
- artigo científico
- sistema industrial
- startup
- monitoramento ocupacional inteligente

