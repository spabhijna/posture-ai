import cv2
import os
import argparse
import supervision as sv

# Assuming these are defined in separate modules
from model import PoseModel
from check_pose import PoseChecker
from visualizer import Visualizer
from supervision import KeyPoints

def main(input_path, display=False, scale=3):
    # Initialize components
    model = PoseModel("../models/yolov8s-pose.pt")
    checker = PoseChecker()
    visualizer = Visualizer()

    # Determine if input is an image or video
    _, ext = os.path.splitext(input_path)
    if ext.lower() in ['.jpg', '.jpeg', '.png', '.bmp']:
        is_image = True
    elif ext.lower() in ['.mp4', '.avi', '.mov']:
        is_image = False
    else:
        print(f"Unsupported file type: {ext}")
        return

    # Generate output path
    output_dir = '../output'
    os.makedirs(output_dir, exist_ok=True)
    base_name = os.path.basename(input_path)
    if is_image:
        output_path = os.path.join(output_dir, f"{os.path.splitext(base_name)[0]}_annotated.jpg")
    else:
        output_path = os.path.join(output_dir, f"{os.path.splitext(base_name)[0]}_annotated.mp4")

    if is_image:
        # Process image
        frame = cv2.imread(input_path)
        if frame is None:
            print(f"Error: Could not read image {input_path}")
            return

        # Run pose detection
        results = model.predict(frame)
        keypoints = KeyPoints.from_ultralytics(results)

        # Check poses
        labels = [checker.check_pose(kp) for kp in keypoints.xy if len(kp) > 0]
        # Annotate frame
        annotated_frame = visualizer.annotate_frame(frame, keypoints, labels=labels)

        # Save annotated image
        cv2.imwrite(output_path, annotated_frame)
        print(f"Saved annotated image to {output_path}")

        # Optionally display
        if display:
            visualizer.show(annotated_frame, scale=scale)
            print("Press 'q' to quit the image window.")
            while True:
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    break
            cv2.destroyAllWindows()

    else:
        # Process video
        cap = cv2.VideoCapture(input_path)
        if not cap.isOpened():
            print(f"Error: Could not open video {input_path}")
            return

        # Get video properties
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')

        # Setup video writer
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # Run pose detection
            results = model.predict(frame)
            keypoints = KeyPoints.from_ultralytics(results)

            # Check poses
            labels = [checker.check_pose(kp) for kp in keypoints.xy if len(kp) > 0]

            # Annotate frame
            annotated_frame = visualizer.annotate_frame(frame, keypoints, labels=labels)

            # Write to output video
            out.write(annotated_frame)

            # Optionally display
            if display:
                visualizer.show(annotated_frame, scale=scale)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

        cap.release()
        out.release()
        if display:
            cv2.destroyAllWindows()
        print(f"Saved annotated video to {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Pose Correction Tool")
    parser.add_argument("input", help="Path to input image or video")
    parser.add_argument("--display", action="store_true", help="Display the result")
    parser.add_argument("--scale", type=int, default=3, help="Scale factor for display")
    args = parser.parse_args()

    main(args.input, display=args.display, scale=args.scale)