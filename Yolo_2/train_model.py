if __name__ == "__main__":
    from ultralytics import YOLO
    
    model = YOLO("yolo11n.pt")
    model.train(data="config.yaml", epochs=200, device=0, name="ragnarok_poring_model")
