import sys
import cv2

capture = cv2.VideoCapture(0)
face = cv2.CascadeClassifier('default_frontal_face.xml')

# Validate cascade loaded
if face.empty():
    print("Error: failed to load cascade classifier 'default_frontal_face.xml'.")
    print("Make sure the file exists in the project root or provide the correct path.")
    sys.exit(1)

if not capture.isOpened():
    print("Error: could not open video capture. Check your camera.")
    sys.exit(1)

def _oddize(n: int) -> int:
    """Return an odd integer >= 3 based on n."""
    n = max(3, int(n))
    return n if (n % 2) == 1 else n + 1

while True:
    success, img = capture.read()
    if not success or img is None:
        # Failed to grab frame — stop the loop gracefully
        print("Warning: failed to read frame from camera. Exiting.")
        break

    # Detect on grayscale for better results
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=4)

    if len(faces) == 0:
        cv2.putText(img, 'No Face Found!', (20, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
    else:
        for (x, y, w, h) in faces:
            # Ensure coordinates are within image bounds
            x1, y1 = max(0, x), max(0, y)
            x2, y2 = x1 + w, y1 + h
            image1 = img[y1:y2, x1:x2]
            if image1.size == 0:
                continue

            # Choose a kernel size relative to face width (must be odd)
            k = _oddize(max(3, w // 3))
            gaussian_blurr = cv2.GaussianBlur(image1, (k, k), 0)
            img[y1:y2, x1:x2] = gaussian_blurr

    cv2.imshow('Face Blur', img)
    if cv2.waitKey(1) & 0xff == ord('q'):
        break

capture.release()
cv2.destroyAllWindows()
