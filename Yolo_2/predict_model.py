from ultralytics import YOLO

best_model = 'C:\\Users\\nparo\\OneDrive\\GT - Mahidol\\Class\\2nd\\ITGT523 Computer Vision\\ITGT523_Naddanai\\Yolo_2\\runs\\detect\\ragnarok_poring_model\\weights\\best.pt'
model = YOLO(best_model)
model.predict(source="ragnarok.mp4",    
              show=True,                
              save=True,                
              line_width=2,             
              show_labels=True,         
              show_conf=True,           
              conf=0.50)
