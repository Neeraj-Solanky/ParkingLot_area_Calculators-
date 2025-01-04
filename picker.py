import cv2
import pickle

# Dimensions for horizontal and vertical parking spots
width_horizontal, height_horizontal = 30, 14
width_vertical, height_vertical = 14, 30

try:
    with open('CarParkPos', 'rb') as f:
        posList = pickle.load(f)
except:
    posList = []

def mouseClick(events, x, y, flags, params):
    if events == cv2.EVENT_LBUTTONDOWN:
        # Check if the Shift key is pressed
        if flags & cv2.EVENT_FLAG_SHIFTKEY:
            # Add vertical parking spot
            posList.append((x, y, 'vertical'))
        else:
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
            elif orientation == 'vertical':
                if x1 < x < x1 + width_vertical and y1 < y < y1 + height_vertical:
                    posList.pop(i)
                    break

    # Save updated parking positions
    with open('CarParkPos', 'wb') as f:
        pickle.dump(posList, f)

while True:
    img = cv2.imread('imge.jpg')
    for pos in posList:
        x, y, orientation = pos
        if orientation == 'horizontal':
            cv2.rectangle(img, (x, y), (x + width_horizontal, y + height_horizontal), (255, 0, 255), 2)
        elif orientation == 'vertical':
            cv2.rectangle(img, (x, y), (x + width_vertical, y + height_vertical), (0, 255, 255), 2)

    cv2.imshow("Image", img)
    cv2.setMouseCallback("Image", mouseClick)
    cv2.waitKey(1)