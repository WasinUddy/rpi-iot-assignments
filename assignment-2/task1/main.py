import cv2
import numpy as np

# Create a blank image with white background
height, width = 600, 800
image = np.ones((height, width, 3), dtype=np.uint8) * 255

# Define triangle vertices
pt1 = np.array([400, 100], np.int32)    # Top vertex
pt2 = np.array([200, 500], np.int32)    # Bottom left vertex
pt3 = np.array([600, 500], np.int32)    # Bottom right vertex

# Create array of triangle points
triangle = np.array([pt1, pt2, pt3], np.int32)
triangle = triangle.reshape((-1, 1, 2))

# Draw the triangle
cv2.polylines(image, [triangle], True, (0, 0, 0), 2)

# Write text "homework 2" inside the triangle
text = "homework 2"
font = cv2.FONT_HERSHEY_SIMPLEX
font_scale = 1.0
font_thickness = 2
font_color = (0, 0, 0)  # Black text

# Get text size to center it
text_size = cv2.getTextSize(text, font, font_scale, font_thickness)[0]

# Calculate position to center text inside triangle
text_x = 400 - text_size[0] // 2
text_y = 350 + text_size[1] // 2

# Put text on image
cv2.putText(image, text, (text_x, text_y), font, font_scale, font_color, font_thickness)

# Display the image
cv2.imshow("Triangle with Text", image)

# Wait for a key press and then close
cv2.waitKey(0)
cv2.destroyAllWindows()

# Optionally save the image
cv2.imwrite("triangle_homework2.png", image)
print("Image saved as 'triangle_homework2.png'")

