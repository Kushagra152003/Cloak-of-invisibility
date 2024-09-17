import cv2
import numpy as np
import time

fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi',fourcc,20.0,(640,480))



# Define the color range for detecting the cloak
cloak_color_lower = np.array([0, 0, 40])
cloak_color_upper = np.array([180, 18, 230])

# Initialize the webcam
cap = cv2.VideoCapture(0)
time.sleep(2)
count=0
background= 0
# Allow the camera to warm up and capture the initial background
for i in range(60):
    ret, background = cap.read()
    if not ret:
        break

# Flip the background image (optional based on camera orientation)
background = np.flip(background, axis=1)

# Start the main loop
while True:
    # Capture the current frame
    ret, frame = cap.read()
    if not ret:
        break
    count+=1

    # Flip the frame horizontally (optional based on camera orientation)
    frame = np.flip(frame, axis=1)

    # Convert the frame from BGR to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Create a mask to detect the specific color (cloak color)
    mask = cv2.inRange(hsv, cloak_color_lower, cloak_color_upper)

    # Improve the mask by adding additional lower and upper HSV values for red
    #cloak_color_lower2 = np.array([0, 0, 40])
    #cloak_color_upper2 = np.array([180, 18, 230])
    #mask2 = cv2.inRange(hsv, cloak_color_lower2, cloak_color_upper2)

    # Combine both masks
    #mask = mask1 + mask2

    # Refine the mask using morphological transformations
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8), iterations=2)
    mask = cv2.morphologyEx(mask, cv2.MORPH_DILATE, np.ones((3, 3), np.uint8), iterations=1)

    # Invert the mask to get the parts of the frame that are not the cloak
    mask_inv = cv2.bitwise_not(mask)

    # Update the background continuously for regions where the cloak is detected
    cloak_area = cv2.bitwise_and(background, background, mask=mask)

    # Extract the current frame's area that does not include the cloak
    non_cloak_area = cv2.bitwise_and(frame, frame, mask=mask_inv)

    # Combine the cloak area with the non-cloak area
    final_output = cv2.addWeighted(cloak_area, 1, non_cloak_area, 1, 0)
    out.write(final_output)
    # Display the final output
    cv2.imshow("Invisibility Cloak", final_output)

    # Update the background for the next iteration
    #background = frame.copy()

    # Break the loop when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
