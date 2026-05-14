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