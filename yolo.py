import cv2
import numpy as np
from ultralytics import YOLO
import time

# 1. Configurações de Modelos e Janela
model_pose = YOLO('yolov8n-pose.pt')
cap = cv2.VideoCapture(0)

win_name = "ROBOTGAMES - MONITORAMENTO ERGONOMICO"
cv2.namedWindow(win_name, cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty(win_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

# Variáveis de monitoramento (10 segundos)
tempo_sentado = 0
tempo_cintura = 0
limite_alerta = 10.0 # Segundos configurados para o TCC

def draw_modern_ui(img, t_sentado, t_cintura):
    """ Cria um painel lateral com estética Roxo e Rosa """
    h, w, _ = img.shape
    panel_w = 350
    # Painel com fundo gradiente ou sólido escuro
    panel = np.zeros((h, panel_w, 3), dtype=np.uint8)
    panel[:] = (25, 10, 25) # Roxo bem escuro de fundo

    # Cores da Paleta
    ROXO_VIVO = (255, 0, 150)  # Magenta/Roxo
    ROSA_NEON = (180, 100, 255) # Rosa Neon
    BRANCO = (240, 240, 240)
    CINZA_BORDA = (60, 40, 60)

    # Título do Dashboard
    cv2.putText(panel, "WANDI VISION", (30, 50), cv2.FONT_HERSHEY_DUPLEX, 1.2, ROXO_VIVO, 2)
    cv2.putText(panel, "Analise de Fadiga", (30, 80), 1, 1, ROSA_NEON, 1)
    cv2.line(panel, (30, 100), (320, 100), CINZA_BORDA, 1)

    # --- WIDGET 1: POSICAO SENTADA ---
    # Barra de progresso Sentado
    perc_sentado = int((t_sentado / limite_alerta) * 280)
    cv2.putText(panel, "POSTURA SENTADA", (30, 150), 1, 1.1, BRANCO, 1)
    cv2.rectangle(panel, (30, 165), (310, 185), CINZA_BORDA, -1) # Fundo da barra
    color_s = ROSA_NEON if t_sentado < limite_alerta else (0, 0, 255) # Rosa vira Vermelho no alerta
    cv2.rectangle(panel, (30, 165), (30 + perc_sentado, 185), color_s, -1)
    cv2.putText(panel, f"{int(t_sentado)}s / 10s", (30, 210), 1, 1, ROSA_NEON, 1)
    if t_sentado >= limite_alerta:
        cv2.putText(panel, "ALERTA: IMOBILIDADE", (30, 235), 1, 1, (0, 0, 255), 2)

    # --- WIDGET 2: MAOS NA CINTURA ---
    # Barra de progresso Cintura
    perc_cintura = int((t_cintura / limite_alerta) * 280)
    cv2.putText(panel, "MAOS NA CINTURA", (30, 320), 1, 1.1, BRANCO, 1)
    cv2.rectangle(panel, (30, 335), (310, 355), CINZA_BORDA, -1)
    color_c = ROXO_VIVO if t_cintura < limite_alerta else (0, 0, 255)
    cv2.rectangle(panel, (30, 335), (30 + perc_cintura, 355), color_c, -1)
    cv2.putText(panel, f"{int(t_cintura)}s / 10s", (30, 380), 1, 1, ROXO_VIVO, 1)
    if t_cintura >= limite_alerta:
        cv2.putText(panel, "ALERTA: SOBRECARGA", (30, 405), 1, 1, (0, 0, 255), 2)

    # Rodapé Técnico
    cv2.putText(panel, "ENGINEER: LUAMBA", (30, h-30), 1, 0.8, (100, 100, 100), 1)

    return np.hstack((img, panel))

while cap.isOpened():
    success, frame = cap.read()
    if not success: break

    frame = cv2.resize(frame, (800, 600))
    results = model_pose(frame, imgsz=320, conf=0.5, verbose=False)

    esta_sentado = False
    esta_na_cintura = False

    for r in results:
        # Desenhar o esqueleto com cores personalizadas (opcional)
        frame = r.plot(boxes=False)
        
        if r.keypoints is not None:
            kpts = r.keypoints.xy.cpu().numpy()[0]
            
            if len(kpts) > 12:
                # 1. Lógica: Sentado (Quadril 11/12 quase na mesma altura dos Joelhos 13/14)
                # Na visão frontal, a distância vertical entre quadril e joelho encurta
                dist_vertical_sentado = abs(kpts[11][1] - kpts[13][1])
                if dist_vertical_sentado < 60: # Ajuste conforme a distância da câmera
                    esta_sentado = True

                # 2. Lógica: Mãos na Cintura (Pulsos 9/10 perto dos Quadris 11/12)
                dist_p_c_esq = np.linalg.norm(kpts[9] - kpts[11])
                dist_p_c_dir = np.linalg.norm(kpts[10] - kpts[12])
                if dist_p_c_esq < 50 and dist_p_c_dir < 50:
                    esta_na_cintura = True

    # Atualização dos contadores (Frequência aproximada de 10 FPS no processamento)
    if esta_sentado:
        tempo_sentado = min(limite_alerta, tempo_sentado + 0.1)
    else:
        tempo_sentado = max(0, tempo_sentado - 0.2)

    if esta_na_cintura:
        tempo_cintura = min(limite_alerta, tempo_cintura + 0.1)
    else:
        tempo_cintura = max(0, tempo_cintura - 0.2)

    # Gerar a UI combinada
    final_view = draw_modern_ui(frame, tempo_sentado, tempo_cintura)

    cv2.imshow(win_name, final_view)
    if cv2.waitKey(1) & 0xFF == ord('q'): break

cap.release()
cv2.destroyAllWindows()