import cv2 
import pickle
import cvzone
import numpy as np

# Load the static image
img = cv2.imread('imge.jpg')

# Load saved parking positions
with open('CarParkPos', 'rb') as f:
    posList = pickle.load(f)

# Dimensions for parking spots
width_horizontal, height_horizontal = 30, 14
width_vertical, height_vertical = 14, 30


def checkParkingSpace(imgPro):
    spaceCounter = 0
    totalParkingLotArea = 0  # Variable to store the total area of the parking lot

    for pos in posList:
        x, y, orientation = pos  # Unpack the tuple to x, y, and orientation

        # Crop the image for the parking space
        if orientation == 'horizontal':
            imgCrop = imgPro[y:y + height_horizontal, x:x + width_horizontal]
        elif orientation == 'vertical':
            imgCrop = imgPro[y:y + height_vertical, x:x + width_vertical]

        count = cv2.countNonZero(imgCrop)  # Count non-black pixels

        # If fewer pixels are occupied (parking space is free)
        if count < 265:
            color = (0, 255, 0)  # Green color for free
            thickness = 5
            spaceCounter += 1
        else:
            color = (0, 0, 255)  # Red color for occupied
            thickness = 2

        # Draw rectangle around parking space
        cv2.rectangle(img, pos[:2], (pos[0] + width_horizontal, pos[1] + height_horizontal), color, thickness)

        # Show count of occupied pixels in the space
        cvzone.putTextRect(img, str(count), (x, y + height_horizontal - 3), scale=1, thickness=2, offset=0, colorR=color)

    # Calculate the total parking lot area in square feet
    totalArea = len(posList) * 128  # Each slot is 128 square feet (16x8)

    # Display the count of free spaces and the total parking lot area
    cvzone.putTextRect(img, f'Free: {spaceCounter}/{len(posList)}', (100, 50), scale=3, thickness=5, offset=20, colorR=(255, 255, 0), colorT=(0, 0, 0))
    cvzone.putTextRect(img, f'Total Area: {totalArea} sq ft', (100, 100), scale=2, thickness=4, offset=20, colorR=(0, 255, 255),colorT=(0, 0, 0))


def mouseClick(events, x, y, flags, params):
    if events == cv2.EVENT_LBUTTONDOWN:
        # Add horizontal parking spot
        posList.append((x, y, 'horizontal'))
    elif events == cv2.EVENT_RBUTTONDOWN:
        # Remove a parking spot (nearest match based on type and location)
        for i, pos in enumerate(posList):
            x1, y1, orientation = pos
            if orientation == 'horizontal':
                if x1 < x < x1 + width_horizontal and y1 < y < y1 + height_horizontal:
                    posList.pop(i)
                    break
            

    # Save updated parking positions
    with open('CarParkPos', 'wb') as f:
        pickle.dump(posList, f)

while True:
    # Preprocess the image for parking space detection
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 1)
    imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                         cv2.THRESH_BINARY_INV, 25, 16)
    imgMedian = cv2.medianBlur(imgThreshold, 5)
    kernel = np.ones((3, 3), np.uint8)
    imgDilate = cv2.dilate(imgMedian, kernel, iterations=1)

    # Check for parking space status
    checkParkingSpace(imgDilate)

    # Display the processed image
    cv2.imshow("Parking Area", img)
    cv2.setMouseCallback("Parking Area", mouseClick)  # Enable mouse click callback to add/remove spots

    # Wait for a key press to proceed to the next frame
    key = cv2.waitKey(100)  # Use 100 ms delay for smooth frame transitions
    if key == ord('q'):  # Press 'q' to quit the loop
        break