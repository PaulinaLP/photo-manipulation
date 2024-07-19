from image_utils import convert_heic_to_jpeg, resize_image, change_background_to_white

CONVERT=0
# Paths
path = 'input/photo2.JPG'
jpeg_path = 'output/converted_image.jpg'
resized_path = 'output/resized_image.jpg'
final_output_path = 'output/final_carnet_image.jpg'

# Convert HEIC to JPEG
if CONVERT ==1:
    convert_heic_to_jpeg(path, jpeg_path)
    print(f"Converted HEIC to JPEG: {jpeg_path}")

if CONVERT ==1:
    change_background_to_white(jpeg_path, final_output_path)
    print(f"Changed background to white: {final_output_path}")    
else:
    change_background_to_white(path, final_output_path)
    print(f"Changed background to white: {final_output_path}")
   
resize_image(final_output_path, resized_path, crop_direction='top')
print(f"Resized image to tamaño carnet: {resized_path}")



