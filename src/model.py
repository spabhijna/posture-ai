from ultralytics import YOLO


class PoseModel:
    def __init__(self, path):
        self.model = YOLO(path)

    def predict(self, frame):
        return self.model.predict(frame)[0]
