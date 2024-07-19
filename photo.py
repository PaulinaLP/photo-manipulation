from image_utils import convert_heic_to_jpeg, resize_image, change_background_to_white

CONVERT=0
# Paths
path = 'input/photo1.JPG'
jpeg_path = 'output/converted_image.jpg'
resized_path = 'output/resized_image.jpg'
background_path = 'output/final_carnet_image.jpg'

# Convert HEIC to JPEG
if CONVERT ==1:
    convert_heic_to_jpeg(path, jpeg_path)
    print(f"Converted HEIC to JPEG")
    path = jpeg_path

resize_image(path, resized_path, crop_direction='top')
print(f"Resized image to tamaño carnet")
path = resized_path

change_background_to_white(path, background_path)
print(f"Changed background to white") 
path =  background_path  
   




