import torch
import cv2

model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained = True)

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame, size=640)

    annotated_frame = results.render()[0]

    cv2.imshow('YOLOv5 - Phone Camera', annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
