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

    requires-python >=3.11

    numpy<2.0
    opencv-python>=4.11.0.86
    supervision<0.25.0
    torch==2.0.1
    torchaudio==2.0.2
    torchvision==0.15.2
    ultralytics>=8.3.82

### Setup

1. Clone the repository:
   ```
   git clone https://github.com/spabhijna/Correct_Pose_Detection.git
   cd Correct_Pose_Detection
   ```

2. Install dependencies:
   ```
   pip install uv  # Install uv if not already installed
   uv venv .venv  # Create a virtual environment
   source .venv/bin/activate  # Activate the environment (Linux/macOS)
   # On Windows, use: .venv\Scripts\activate
   uv install  # Install dependencies from pyproject.toml
   
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
└── pyproject.toml        # Project details with dependencies
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

![image](https://github.com/user-attachments/assets/d26618d7-89ef-45b6-b9d8-468f3c2fc401)


*Worker performing a lifting task*

### Output Image

![image_annotated](https://github.com/user-attachments/assets/670f6f7b-304c-40c7-a5d7-80ee61208214)


*Annotated output showing detected keypoints and ergonomic assessment*

In this example, the system detects several ergonomic issues:
- Back angle of 69.1° (above threshold of 20°)
- Knee angle of 179.1° (above recommended range of (90°,120°))
- Head angle of 90.2° (above threshold of 15°)
- Elbow angle of 166.5 (above recommended range of (70°,110°))

The annotated output displays these issues directly on the image, with green text for incorrect postures helping workers and supervisors identify and correct ergonomic problems in real-time.

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

## Acknowledgments

- The project uses YOLOv8 from Ultralytics for pose estimation
- Supervision library for visualization helpers
