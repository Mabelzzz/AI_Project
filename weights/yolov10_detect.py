import cv2
import time
from ultralytics import YOLOv10

def yolov10_inference(frame, model, image_size, conf_threshold):
    results = model.predict(source=frame, imgsz=image_size, conf=conf_threshold)
    frame = results[0].plot()
    return frame

def main();
    image_size = 640
    conf_threshold = 0.25
    model = YOLOv10("yolov10n.pt")
    source = "overhead.mp4"
    cap = cv2.VideoCapture(source)
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return
    while True:
        ret, frame = cap.read()
        start_time = time.time()
        if not ret:
            break
        frame = yolov10_inference(frame, model, image_size, conf_threshold)
        end_time = time.time()
        fps = 1/(end_time - start_time)
        framefps = "FPS: {:.2f}".format(fps)
        cv2.rectangle(frame, (10, 1), (120, 20), (0, 0, 0), -1)
        cv2.putText(frame, framefps, (15, 17), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
        cv2.imshow("YOLOv10 Object Detection", frame)
        if cv2.waitKey(1) & OxFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
main()