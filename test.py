import cv2

# Global variables to track mouse events
start_x, start_y = -1, -1
end_x, end_y = -1, -1
drawing = False

def draw_rectangle(event, x, y, flags, param):
    global start_x, start_y, end_x, end_y, drawing, image_copy

    if event == cv2.EVENT_LBUTTONDOWN:
        start_x, start_y = x, y
        end_x, end_y = x, y
        drawing = True

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            end_x, end_y = x, y
            image_copy = image.copy()
            cv2.rectangle(image_copy, (start_x, start_y), (end_x, end_y), (0, 255, 0), 2)

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False

# Load your image here
image = cv2.imread("test.png")
image_copy = image.copy()

cv2.namedWindow("Image")
cv2.setMouseCallback("Image", draw_rectangle)

while True:
    cv2.imshow("Image", image_copy)
    key = cv2.waitKey(1) & 0xFF

    if key == 27:  # Press 'Esc' to exit
        break
    

cv2.destroyAllWindows()
