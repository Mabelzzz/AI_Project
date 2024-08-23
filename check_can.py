import cv2
import torch

def check_can(image_path, model_path='weights/best2_can.pt'):
    """
    Checks if an object in the image is a can.

    Parameters:
        image_path (str): Path to the input image.
        model_path (str): Path to the YOLO model weights.

    Returns:
        bool: True if a can is detected, False otherwise.
    """
    # Load YOLO model
    model = torch.hub.load('ultralytics/yolov10', 'custom', path='weights/best2_can.pt', source='local')

    # Load and preprocess image
    img = cv2.imread(image_path)
    results = model(img)

    # Check if any detections are classified as 'can'
    labels = results.names
    detected_classes = results.xyxy[0][:, -1].tolist()  # Get detected class indices
    detected_labels = [labels[int(cls)] for cls in detected_classes]  # Convert to class names

    return 'can' in detected_labels

# if __name__ == "__main__":
#     import sys
#     if len(sys.argv) != 2:
#         print("Usage: python check_can.py <image_path>")
#         sys.exit(1)

#     image_path = sys.argv[1]
#     is_can = check_can(image_path)
#     print(f"Is it a can? {'Yes' if is_can else 'No'}")
