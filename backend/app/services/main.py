import sys
import cv2
import numpy as np
from datetime import datetime
import os

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

# Get camera properties for video writer
frame_width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = int(capture.get(cv2.CAP_PROP_FPS)) or 30

# Blur type selection
blur_type = 'gaussian'  # 'gaussian', 'mosaic', or 'none'
blur_enabled = True  # Toggle blur on/off

# Video recording setting
recording = False  # Toggle video recording
video_writer = None
output_dir = 'recordings'

# Create output directory if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

def _oddize(n: int) -> int:
    """Return an odd integer >= 3 based on n."""
    n = max(3, int(n))
    return n if (n % 2) == 1 else n + 1

def apply_gaussian_blur(image: np.ndarray, kernel_factor: int = 3) -> np.ndarray:
    """Apply Gaussian blur to image.

    Args:
        image: Input image
        kernel_factor: Divisor for kernel size calculation

    Returns:
        Blurred image
    """
    h, w = image.shape[:2]
    k = _oddize(max(3, min(h, w) // kernel_factor))
    return cv2.GaussianBlur(image, (k, k), 0)

def apply_mosaic_blur(image: np.ndarray, block_size: int = 10) -> np.ndarray:
    """Apply mosaic (pixelated) blur to image.

    Args:
        image: Input image
        block_size: Size of mosaic blocks in pixels

    Returns:
        Mosaiced image
    """
    h, w = image.shape[:2]
    # Resize down to create mosaic effect
    small_h, small_w = max(1, h // block_size), max(1, w // block_size)
    temp = cv2.resize(image, (small_w, small_h), interpolation=cv2.INTER_LINEAR)
    # Resize back up to original size
    mosaic = cv2.resize(temp, (w, h), interpolation=cv2.INTER_NEAREST)
    return mosaic

def start_recording():
    """Start video recording with timestamp filename."""
    global video_writer
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(output_dir, f'recording_{timestamp}.mp4')
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video_writer = cv2.VideoWriter(filename, fourcc, fps, (frame_width, frame_height))
    if video_writer.isOpened():
        print(f"✓ Recording started: {filename}")
        return True
    else:
        print(f"✗ Failed to start recording")
        video_writer = None
        return False

def stop_recording():
    """Stop video recording."""
    global video_writer
    if video_writer is not None:
        video_writer.release()
        video_writer = None
        print("✓ Recording stopped")

while True:
    success, img = capture.read()
    if not success or img is None:
        # Failed to grab frame — stop the loop gracefully
        print("Warning: failed to read frame from camera. Exiting.")
        break

    # Apply mirror/flip (always enabled)
    img = cv2.flip(img, 1)  # 1 = flip horizontally (left-right)

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

            # Apply blur if enabled
            if blur_enabled:
                if blur_type == 'gaussian':
                    k = _oddize(max(3, w // 3))
                    blurred = cv2.GaussianBlur(image1, (k, k), 0)
                elif blur_type == 'mosaic':
                    mosaic_block_size = max(3, w // 15)
                    blurred = apply_mosaic_blur(image1, block_size=mosaic_block_size)

                img[y1:y2, x1:x2] = blurred

    # Write frame to video file if recording
    if recording and video_writer is not None:
        video_writer.write(img)

    # Display current status
    blur_status = 'OFF' if not blur_enabled else blur_type.upper()
    recording_status = 'REC' if recording else 'OFF'
    mode_text = f'Blur: {blur_status} | Rec: {recording_status} | [G]ussian [M]osaic [B]lur [R]ec [Q]uit'
    cv2.putText(img, mode_text, (10, img.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

    cv2.imshow('Face Blur', img)

    # Handle keyboard input
    key = cv2.waitKey(1) & 0xff
    if key == ord('q'):
        break
    elif key == ord('g'):
        blur_type = 'gaussian'
        blur_enabled = True
        print("✓ Switched to Gaussian Blur mode (ENABLED)")
    elif key == ord('m'):
        blur_type = 'mosaic'
        blur_enabled = True
        print("✓ Switched to Mosaic Blur mode (ENABLED)")
    elif key == ord('b'):
        blur_enabled = not blur_enabled
        status = "ENABLED" if blur_enabled else "DISABLED"
        print(f"✓ Blur {status}")
    elif key == ord('r'):
        recording = not recording
        if recording:
            start_recording()
        else:
            stop_recording()

if recording:
    stop_recording()

capture.release()
cv2.destroyAllWindows()
