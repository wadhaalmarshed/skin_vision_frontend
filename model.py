from ultralytics import YOLO

model = YOLO("yolov8n.yaml")

results = model.train(data="/home/harrison/code/mclordm/skin_vision/models/model.yaml", epochs=5)
