from PIL import Image
from rembg import remove
from PIL import Image, ImageFilter
import numpy as np

# https://www.geeksforgeeks.org/how-to-remove-the-background-from-an-image-using-python/
# https://stackoverflow.com/questions/76077451/extract-the-background-in-an-image-and-save

input_path = 'person.jpg'
extracted_path = 'extracted_image.png'
extracted_bg_path = 'extracted_bg.png'
filtered_bg_path = 'filtered_bg.png'
final_path = 'final-image.png'

input = Image.open(input_path)
extracted_image = remove(input)
# extracted_image.save(extracted_path)

# Convert PIL to NumPy (keep only RGB channels).
input_rgb = np.array(input)[:, :, 0:3]
output_rgba = np.array(extracted_image)  # Convert PIL to NumPy.
alpha = output_rgba[:, :, 3]  # Extract alpha channel.
alpha3 = np.dstack((alpha, alpha, alpha))  # Convert to 3 channels

extracted_bg_rgb = input_rgb.astype(
    np.float64) * (1 - alpha3.astype(np.float64)/255)  # Multiply by 1-alpha
extracted_bg_rgb = extracted_bg_rgb.astype(np.uint8)  # Convert back to uint8

extracted_bg = Image.fromarray(extracted_bg_rgb)
extracted_bg = extracted_bg.convert("RGBA")
# extracted_bg.save(extracted_bg_path)

# Apply filters to extracted_bg
filtered_bg = extracted_bg.filter(ImageFilter.BLUR)
# filtered_bg.save(filtered_bg_path)

result = Image.alpha_composite(filtered_bg, extracted_image)

# Save the result
result.save(final_path)
