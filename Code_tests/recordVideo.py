import cv2

streamlink = "http://192.168.1.104:81/stream"
cap = cv2.VideoCapture(streamlink)
print(cap.get(3),cap.get(4))
out = cv2.VideoWriter("outpy.avi",cv2.VideoWriter_fourcc('M','J','P','G'), 30, (int(cap.get(3)),int(cap.get(4))))
while True:
      ret, frame = cap.read()

      if ret:
            out.write(frame)
            cv2.imshow('Video', frame)
            if cv2.waitKey(1) == ord('q'):
                break

cap.release()
cv2.destroyAllWindows()

    #   frame = frame[:100,:100]
       