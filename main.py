from ultralytics import YOLO
from ultralytics.solutions import object_counter
import cv2
import serial
import time

# Initialize serial connection with Arduino
arduino = serial.Serial('COM5', 9600)
time.sleep(2)  # Wait for Arduino to initialize

def send_to_arduino(detections):
    """
    Send object count to Arduino via serial connection.

    Args:
        detections (int): Number of detected objects.
    """
    print("Detections : ",detections)
    count_str = str(detections)
    count_bytes = count_str.encode()  # Convert string to bytes

    arduino.write(count_bytes + b"\n")  # Send data to Arduino

def rescale_frame(frame, percent=175):
    """
    Rescale frame to a certain percentage of its original size.

    Args:
        frame (numpy.ndarray): Input frame.
        percent (int): Percentage to scale the frame.

    Returns:
        numpy.ndarray: Rescaled frame.
    """
    width = int(frame.shape[1] * percent/ 100)
    height = int(frame.shape[0] * percent/ 100)
    dim = (width, height)
    return cv2.resize(frame, dim, interpolation =cv2.INTER_AREA)

def main():
    # Initialize YOLO model
    model = YOLO("yolov8n.pt")

    # Open video capture device
    cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)  # Change the index according to your camera
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)  # Set frame width
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)  # Set frame height

    # Check if camera is opened successfully
    assert cap.isOpened(), "Error reading video file"

    # Get video properties
    w, h, fps = (int(cap.get(x)) for x in (cv2.CAP_PROP_FRAME_WIDTH, cv2.CAP_PROP_FRAME_HEIGHT, cv2.CAP_PROP_FPS))

    # Define line points for counting objects
    line_points = [(640, 0), (640, 1000)]  # Adjust the line points according to your setup
    classes_to_count = [2]  # 0: person, 2: car, 67: cell phone

    # Initialize Object Counter
    counter = object_counter.ObjectCounter()
    counter.set_args(view_img=True,
                     reg_pts=line_points,
                     classes_names=model.names,
                     draw_tracks=True,
                     line_thickness=2,view_in_counts=False)

    # Main loop for processing video frames
    while cap.isOpened():
        success, im0 = cap.read()
        frame = rescale_frame(im0, percent=175)  # Rescale frame for better processing
        frame = cv2.flip(frame, 1)  # Flip the frame horizontally if needed

        if not success:
            print("Video frame is empty or video processing has been successfully completed.")
            break

        # Track objects using YOLO model
        tracks = model.track(frame, persist=True,show=False,verbose=True, classes=classes_to_count)

        # Count objects and update counts
        frame = counter.start_counting(frame, tracks)
        send_to_arduino(counter.out_counts)  # Send object counts to Arduino

    # Release video capture and close all windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
