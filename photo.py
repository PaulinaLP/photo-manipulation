from image_utils import convert_heic_to_jpeg, resize_image, change_background_to_white
import os 

CONVERT=1
RESIZE=0
CHANGE=0
# Path
path = 'input'

# Loop through the folder
for filename in os.listdir(path):
    file_path = os.path.join(path, filename)  
    file_name = file_path[:-5]

    # Convert HEIC to JPEG
    if CONVERT ==1:
        jpeg_path = 'output/converted_image'+file_name+'.jpg'
        convert_heic_to_jpeg(file_path, jpeg_path)
        print(f"Converted HEIC to JPEG")
        path = jpeg_path

    if RESIZE  ==1:
        resized_path = 'output/resized_image'+file_name+'.jpg'
        resize_image(path, resized_path, crop_direction='top')
        print(f"Resized image to tamaño carnet")
        path = resized_path

    if CHANGE ==1:
        background_path= 'output/nobackground_image'+file_name+'.jpg'
        change_background_to_white(path, background_path)
        print(f"Changed background to white") 
        path =  background_path     
    




