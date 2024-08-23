from ultralytics import YOLO

# Load a pre-trained YOLOv10n model
model = YOLO("weights/best1_bottle.pt") # Your model should be here after training 

# Perform object detection on an image
results = model("bottle.jpeg") 
# results = model("image.jpg") 

# image you weant to predict on
# bottleModel = model.names
# Display the results
results[0].show()
# for i in results:
#     print(i)
print("Result.Boxes: ", results[0].boxes)


# print("Result.Name: ", results[0].names)
# print("Result: ", results)


# Check if there are any detections
if len(results[0].boxes) == 0:
    # raise HTTPException(status_code=400, detail="Invalid image format")
    print("No detections")
else:
    print("Detections found:")
    isValidBottle = True
    for detection in results[0].boxes:
        box = detection.xyxy.numpy()  # Bounding box coordinates in (x1, y1, x2, y2) format
        confidence = detection.conf.numpy()  # Confidence score
        cls = int(detection.cls.numpy())  # Class label index
        bottleModel = model.names[cls]  # Get the class name
        print(f"Box: {box}, Confidence: {confidence}, Class: {bottleModel}")