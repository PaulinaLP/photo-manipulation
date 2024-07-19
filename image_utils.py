from PIL import Image, ImageOps
import pyheif
import numpy as np
import cv2

def convert_heic_to_jpeg(heic_path, jpeg_path):
    # Open the HEIC file
    heif_file = pyheif.read(heic_path)
    image = Image.frombytes(
        heif_file.mode, 
        heif_file.size, 
        heif_file.data, 
        "raw", 
        heif_file.mode, 
        heif_file.stride,
    )
    
    # Save as JPEG
    image.save(jpeg_path, "JPEG")

def resize_image(image_path, output_path, width_mm=26, height_mm=32, dpi=300, crop_direction='right'):
    # Open the image
    image = Image.open(image_path)
    
    # Calculate the target width and height in pixels
    width_px = int((width_mm / 25.4) * dpi)
    height_px = int((height_mm / 25.4) * dpi)
    
    # Crop the image to the correct aspect ratio
    aspect_ratio = width_px / height_px
    original_width, original_height = image.size
    original_aspect_ratio = original_width / original_height
    
    if original_aspect_ratio > aspect_ratio:
        # Image is too wide, crop the sides
        new_width = int(aspect_ratio * original_height)
        if crop_direction == 'left':
            left = 0
        else:
            left = original_width - new_width
        right = left + new_width
        top = 0
        bottom = original_height
    else:
        # Image is too tall, crop the top or bottom
        new_height = int(original_width / aspect_ratio)
        if crop_direction == 'top':
            top = 0
        else:
            top = original_height - new_height
        bottom = top + new_height
        left = 0
        right = original_width
    
    image = image.crop((left, top, right, bottom))
    
    # Resize the image to the specified size
    image = image.resize((width_px, height_px), Image.Resampling.LANCZOS)
    
    # Save the resized image
    image.save(output_path, "JPEG")


def fill_below_black_pixels(mask, center_width_start, center_width_end, start_pic = 800):
    """
    Fill all pixels below the first black pixel in each column within the central 50% of the image width.
    """
    height, width = mask.shape  
    print(center_width_start)
    # Iterate over each column within the central part of the image
    for x in range(center_width_start, center_width_end):
        found_black = False
        # Start scanning from the top of the image
        for y in range(height):
            if mask[y, x] == 0:  # Detect the first black pixel
                found_black = True
            if found_black:
                mask[y, x] = 0  # Fill below the first black pixel
    for x in range(0, start_pic):       
        for y in range(height):
            mask[y, x] = 255  # Fill below the first black pixel
    return mask


def change_background_to_white(image_path, output_path, white_threshold=120, gray_threshold=40):
    # Open the image and convert to RGBA
    image = Image.open(image_path).convert('RGBA')
    
    # Convert image to numpy array
    data = np.array(image)
    
    # Convert to grayscale
    gray = cv2.cvtColor(data, cv2.COLOR_RGBA2GRAY)
    
    # Use Otsu's thresholding to create a binary mask of the silhouette
    _, binary_mask = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    # Find contours
    contours, _ = cv2.findContours(binary_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Create a mask of the silhouette
    silhouette_mask = np.zeros_like(binary_mask)   
    cv2.drawContours(silhouette_mask, contours, -1, (255), thickness=cv2.FILLED)   

    # Adjust silhouette mask: fill all pixels below the first black pixel in each column within the central 50% of the image height
    height, width = silhouette_mask.shape
    center_width_start = int(width  * 0.35)
    center_width_end = int(width  * 0.65)
    adjusted_silhouette_mask = fill_below_black_pixels(silhouette_mask.copy(), center_width_start, center_width_end)
    print(adjusted_silhouette_mask)
    
    # Save the adjusted silhouette mask for visualization
    adjusted_silhouette_image_path = "adjusted_silhouette_mask.jpg"
    cv2.imwrite(adjusted_silhouette_image_path, adjusted_silhouette_mask)
    print(f"Adjusted silhouette mask saved to {adjusted_silhouette_image_path}.")
    
    near_white_mask = (data[..., 0] > white_threshold) & (data[..., 1] > white_threshold) & (data[..., 2] > white_threshold)
    
    # Define near-gray mask
    # For near-gray, we consider the pixels where the RGB values are close to each other
    gray_mask = np.abs(data[..., 0] - data[..., 1]) < gray_threshold
    gray_mask &= np.abs(data[..., 1] - data[..., 2]) < gray_threshold
    gray_mask &= np.abs(data[..., 0] - data[..., 2]) < gray_threshold
    
    # Combine near-white and near-gray masks
    combined_mask = near_white_mask | gray_mask 
    
    # Invert the silhouette mask to get the background mask
    background_mask = adjusted_silhouette_mask == 255   
    
    # Combine the near-white mask with the background mask
    final_mask = combined_mask & background_mask
    
    # Replace near-white pixels with white only in the background
    data[final_mask, :3] = 255
    
    # Create a new image from the modified array
    new_image = Image.fromarray(data, 'RGBA').convert('RGB')
    
    # Save the new image
    new_image.save(output_path, "JPEG")
