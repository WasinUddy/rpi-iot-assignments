import cv2
import os

def detect_faces_webcam():
    """
    Detect faces in real-time using webcam with Haar Cascade classifier.
    Press 'q' to exit the application.
    """
    # Load the pre-trained Haar Cascade classifier for face detection
    script_dir = os.path.dirname(os.path.abspath(__file__))
    cascade_path = os.path.join(script_dir, 'haarcascade_frontalface_default.xml')
    face_cascade = cv2.CascadeClassifier(cascade_path)


    if face_cascade.empty():
        print("Error: Could not load face cascade classifier")
        return

    # Initialize webcam (0 is the default camera)
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open webcam")
        return

    print("Face Detection Started")
    print("Press 'q' to exit")
    print("Press 's' to save a frame with detected faces")

    frame_count = 0

    while True:
        # Read frame from webcam
        ret, frame = cap.read()

        if not ret:
            print("Error: Failed to read frame")
            break

        frame_count += 1

        # Convert to grayscale for detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces
        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            maxSize=(300, 300)
        )

        # Draw rectangles around detected faces
        face_count = 0
        for (x, y, w, h) in faces:
            face_count += 1

            # Draw face rectangle
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Label the face
            cv2.putText(frame, f'Face {face_count}', (x, y - 10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)


        # Display frame information
        cv2.putText(frame, f'Faces: {face_count}', (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(frame, f'Frame: {frame_count}', (10, 70),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        # Display the frame
        cv2.imshow('Face Detection', frame)

        # Check for key press
        key = cv2.waitKey(1) & 0xFF

        if key == ord('q'):
            print("Exiting face detection...")
            break
        elif key == ord('s'):
            # Save the frame with detected faces
            output_dir = os.path.dirname(os.path.abspath(__file__))
            filename = os.path.join(output_dir, f'face_detection_{frame_count}.jpg')
            cv2.imwrite(filename, frame)
            print(f"Frame saved: {filename}")

    # Release resources
    cap.release()
    cv2.destroyAllWindows()
    print("Face detection completed")


if __name__ == "__main__":
    detect_faces_webcam()

