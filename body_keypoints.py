import cv2
import json

# Mount Google Drive if needed
# from google.colab import drive
# drive.mount('/content/drive')

# Define paths to OpenPose model files
prototxt_path = "/content/openpose/models/pose_deploy.prototxt"
caffemodel_path = "/content/openpose/models/pose_iter_400000.caffemodel"

# Load OpenPose model
net = cv2.dnn.readNetFromCaffe(prototxt_path, caffemodel_path)

# Function to perform pose estimation on an image
def detect_pose(image_path):
    # Read the input image
    image = cv2.imread(image_path)
    
    if image is None:
        print(f"Error: Unable to read image from {image_path}")
        return None
    
    # Resize image to match OpenPose input size (default: 368x368)
    input_width, input_height = 368, 368
    image_resized = cv2.resize(image, (input_width, input_height))

    # Create blob from the image
    blob = cv2.dnn.blobFromImage(image_resized, 1.0 / 255.0, (input_width, input_height), (0, 0, 0), swapRB=False, crop=False)

    # Set input to the network
    net.setInput(blob)

    # Perform forward pass to get outputs
    output = net.forward()

    # Extract pose keypoints from the output
    keypoints = []
    for i in range(18):  # Assuming 18 keypoints for pose estimation
        x = int(output[0][i][0])
        y = int(output[0][i][1])
        confidence = float(output[0][i][2])
        keypoints.extend([x, y, confidence])

    # Prepare JSON output in the specified format
    json_output = {
        "version": 1.0,
        "people": [
            {
                "face_keypoints": [],
                "pose_keypoints": keypoints,
                "hand_right_keypoints": [],
                "hand_left_keypoints": []
            }
        ]
    }

    return json_output

# Input image path (replace with your image path)
input_image_path = "/content/man.jpg"

# Perform pose detection and get JSON output
json_result = detect_pose(input_image_path)

if json_result is not None:
    # Print or save the JSON output
    print(json.dumps(json_result, indent=4))
else:
    print("Pose detection failed.")