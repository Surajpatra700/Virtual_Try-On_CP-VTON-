import PIL.Image as Image
import numpy as np
import cv2

# Replace 'path/to/image.jpg' with your actual image path
image_path = 'C:\\Users\\suraj\\Downloads\\61kzn5AKPLL._AC_UY1100_.jpg'

try:
    # Open image using Pillow for potential format flexibility
    image = Image.open(image_path)

    # Convert to OpenCV BGR format for color manipulation
    image_cv = np.array(image.convert('RGB'))[:, :, ::-1].copy()  # Efficient RGB to BGR conversion
except FileNotFoundError:
    print(f"Error: Image file '{image_path}' not found.")
    exit()

hsv_image = cv2.cvtColor(image_cv, cv2.COLOR_BGR2HSV)

# Define color ranges considering variations and lighting conditions
# Experiment with these values to find optimal ranges for your cloth type
color_ranges = [
    # Sample blue cloth range
    (np.array([100, 43, 46]), np.array([124, 255, 255])),
    # Sample red cloth range (adjust Hue values for other colors)
    (np.array([0, 100, 100]), np.array([10, 255, 255])),
]

# Combine masks from multiple color ranges for better coverage (optional)
combined_mask = np.zeros_like(hsv_image[:, :, 0], dtype=np.uint8)  # Initialize empty mask
for lower_color, upper_color in color_ranges:
    mask = cv2.inRange(hsv_image, lower_color, upper_color)
    # Apply morphological operations (optional) to refine mask (e.g., erosion, dilation)
    combined_mask = cv2.bitwise_or(combined_mask, mask)  # Combine masks

# Convert mask back to Pillow Image format if needed
mask_pil = Image.fromarray(combined_mask).convert('L')

# Display or save the mask (optional)
# cv2.imshow('Mask', mask_pil)  # Display mask using OpenCV
mask_pil.save('cloth_mask.jpg')  # Save mask as a grayscale image

