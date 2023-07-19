import cv2
import os

video_path = './outpy.avi'  # Replace with your video file path
output_dir = 'TrainingData'  # Replace with your desired output directory

os.makedirs(output_dir, exist_ok=True)

cap = cv2.VideoCapture(video_path)

frame_count = 0
while True:
    ret, frame = cap.read()

    if not ret:
        break

    # Save the frame as an image
    output_path = os.path.join(output_dir, f"frame_{frame_count}.jpg")
    cv2.imwrite(output_path, frame)

    frame_count += 1

cap.release()
print("Frames saved successfully!")
