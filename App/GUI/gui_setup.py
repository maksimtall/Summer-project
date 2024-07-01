import os

# Get the directory path where this script is located
current_dir = os.path.dirname(os.path.abspath(__file__))

# Define the filenames of your images
image1_filename = 'show_password.png'
image2_filename = 'hide_password.png'

# Construct the paths to your image files relative to the script's location
image1_path = os.path.join(current_dir, image1_filename)
image2_path = os.path.join(current_dir, image2_filename)

# Initialize variables to store image data
image1_data = None
image2_data = None

try:
    # Check if the first image file exists
    if os.path.exists(image1_path):
        # Open the file in binary mode
        with open(image1_path, 'rb') as file1:
            # Read the binary data of the image file
            image1_data = file1.read()
        
        print(f"Image '{image1_filename}' loaded successfully from '{image1_path}'.")
    else:
        print(f"Error: File '{image1_path}' not found.")

    # Check if the second image file exists
    if os.path.exists(image2_path):
        # Open the file in binary mode
        with open(image2_path, 'rb') as file2:
            # Read the binary data of the image file
            image2_data = file2.read()
        
        print(f"Image '{image2_filename}' loaded successfully from '{image2_path}'.")
    else:
        print(f"Error: File '{image2_path}' not found.")

except IOError as e:
    print(f"Error loading image: {e}")

# Now you have image1_data and image2_data containing the binary data of the images
# Use these variables as needed in your application
