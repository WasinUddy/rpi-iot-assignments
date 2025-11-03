import cv2
import numpy as np
import os

def count_coins(image_path):
    """
    Load an image and detect coins using circle detection.
    Circles each coin and marks it with a number.

    Args:
        image_path: Path to the image file
    """
    # Load the image
    image = cv2.imread(image_path)

    if image is None:
        print(f"Error: Could not load image from {image_path}")
        return

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(gray, (9, 9), 2)

    # Detect circles using HoughCircles
    circles = cv2.HoughCircles(
        blurred,
        cv2.HOUGH_GRADIENT,
        dp=1,
        minDist=30,
        param1=50,
        param2=30,
        minRadius=15,
        maxRadius=100
    )

    # Process detected circles
    if circles is not None:
        circles = np.uint16(np.around(circles))
        coin_count = len(circles[0])
        print(f"Number of coins detected: {coin_count}")

        # Draw circles and numbers
        for idx, (x, y, radius) in enumerate(circles[0]):
            # Draw circle outline
            cv2.circle(image, (x, y), radius, (0, 255, 0), 2)

            # Draw a smaller filled circle at center
            cv2.circle(image, (x, y), 3, (0, 0, 255), -1)

            # Put coin number
            coin_number = idx + 1
            cv2.putText(
                image,
                str(coin_number),
                (x - 10, y + 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 255),
                2
            )
    else:
        print("No coins detected")

    # Display the result
    cv2.imshow("Coin Detection", image)

    # Save the output image
    output_path = os.path.join(os.path.dirname(image_path), "output_coins.jpg")
    cv2.imwrite(output_path, image)
    print(f"Output image saved to: {output_path}")

    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return coin_count if circles is not None else 0


if __name__ == "__main__":
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Construct the path to the image
    image_path = os.path.join(script_dir, "images", "0.jpg")

    print(f"Loading image from: {image_path}")
    count_coins(image_path)

