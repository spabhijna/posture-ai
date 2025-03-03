# Correct Pose Detection

A computer vision tool to detect and analyze human posture for workplace safety and ergonomics assessment.

## Description

This project uses pose estimation technology to analyze body posture in images and videos, providing real-time feedback on ergonomic issues. The system is designed to help prevent workplace injuries by identifying incorrect postures and suggesting corrections based on established ergonomic guidelines.

## Features

- Real-time pose detection and analysis
- Support for both image and video inputs
- Comprehensive ergonomic assessment including:
  - Back alignment
  - Knee positioning
  - Head tilt
  - Arm positioning
  - Feet spacing
  - Hip/torso twist
- Visual feedback with annotated outputs
- Customizable thresholds for different ergonomic parameters

## Installation

### Prerequisites

- Python 3.8+
- OpenCV
- NumPy
- PyTorch
- Ultralytics YOLOv8

### Setup

1. Clone the repository:
   ```
   git clone https://github.com/spabhijna/Correct_Pose_Detection.git
   cd Correct_Pose_Detection
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Download the YOLOv8 pose model:
   ```
   mkdir -p models
   # Download YOLOv8s-pose.pt to the models directory
   ```

## Project Structure

```
Correct_Pose_Detection/
├── src/
│   ├── check_pose.py     # Pose analysis algorithms
│   ├── main.py           # Main application entry point
│   ├── model.py          # Pose detection model wrapper
│   ├── utils.py          # Utility functions
│   └── visualizer.py     # Visualization tools
├── models/
│   └── yolov8s-pose.pt   # YOLOv8 pose estimation model
├── input/                # Input images and videos
├── output/               # Output annotated images and videos
└── README.md             # Project documentation
```

## Usage

### Basic Usage

Process an image or video file:

```
python src/main.py input/example.jpg
```

### Display Results

To display the processed results:

```
python src/main.py input/example.mp4 --display
```

### Adjust Display Scale

For better visibility on high-resolution screens:

```
python src/main.py input/example.mp4 --display --scale 2
```

## Example Input and Output

Below is an example showing how the system analyzes posture in a workplace setting:

### Input Image
![Input Image](media/4887339.jpg)
*Worker performing a lifting task*

### Output Image
![Output Image](output/4887339_annotated.jpg)
*Annotated output showing detected keypoints and ergonomic assessment*

In this example, the system detects several ergonomic issues:
- Back angle of 32.7° (exceeds threshold of 20°)
- Knee angle of 85.3° (slightly below recommended range)
- Hip twist of 12.4° (exceeds threshold of 10°)

The annotated output displays these issues directly on the image, with green text for correct postures and red text for incorrect ones, helping workers and supervisors identify and correct ergonomic problems in real-time.

## How It Works

1. **Pose Detection**: Uses YOLOv8 to detect human body keypoints in images or video frames
2. **Ergonomic Analysis**: Analyzes the detected keypoints to check for ergonomic issues
3. **Visualization**: Annotates the input media with visual feedback and ergonomic assessments
4. **Output**: Saves the annotated results and optionally displays them in real-time

## Ergonomic Rules

The system checks the following ergonomic parameters:

- **Back Angle**: Measures the forward bend of the back (threshold: 20°)
- **Knee Angle**: Checks knee flexion (threshold: 90°-120°)
- **Head Angle**: Evaluates head/neck tilt (threshold: 15°)
- **Elbow Angle**: Verifies proper arm positioning (threshold: 70°-110°)
- **Feet Spacing**: Checks stance width relative to shoulders (threshold: 0.6-1.2× shoulder width)
- **Hip Twist**: Measures rotation of torso relative to hips (threshold: 10°)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- The project uses YOLOv8 from Ultralytics for pose estimation
- Supervision library for visualization helpers