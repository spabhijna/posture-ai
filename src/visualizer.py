import cv2
import supervision as sv


class Visualizer:
    def __init__(self):
        self.vertex_annotator = sv.VertexAnnotator()
        self.edge_annotator = sv.EdgeAnnotator()

    def annotate_frame(self, frame, vertices, labels):
        # Create a copy of the frame and annotate vertices and edges
        annotated_frame = self.vertex_annotator.annotate(frame.copy(), vertices)
        annotated_frame = self.edge_annotator.annotate(annotated_frame, vertices)

        # Get frame dimensions
        frame_height, frame_width = frame.shape[:2]

        # Font settings
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.9
        thickness = 2
        max_width = 300  # Maximum width before wrapping text
        spacing = 5  # Space between lines
        padding = 5  # Padding for background rectangle

        # Process each keypoint and label
        for i, kp in enumerate(vertices.xy):
            if len(kp) > 0 and i < len(labels):  # Ensure keypoints and labels exist
                head_pos = kp[0]  # Assume kp[0] is the head keypoint
                label = labels[i]

                # Wrap the text into multiple lines
                words = label.split(" ")
                lines = []
                current_line = []
                for word in words:
                    test_line = " ".join(current_line + [word])
                    text_size = cv2.getTextSize(test_line, font, font_scale, thickness)[
                        0
                    ]
                    if text_size[0] <= max_width:
                        current_line.append(word)
                    else:
                        if current_line:
                            lines.append(" ".join(current_line))
                        current_line = [word]
                if current_line:
                    lines.append(" ".join(current_line))

                if not lines:
                    continue  # Skip if no text lines are generated

                # Calculate text height (approximate)
                text_height = cv2.getTextSize("A", font, font_scale, thickness)[0][1]

                # Calculate total height of the text block
                total_height = (
                    len(lines) * text_height + (len(lines) - 1) * spacing
                    if len(lines) > 1
                    else text_height
                )

                # Determine y-position
                # Try to place above head; if not enough space, place below
                if head_pos[1] - total_height - 10 >= 0:
                    y_start = int(head_pos[1] - total_height - 10)  # Above head
                else:
                    y_start = int(head_pos[1] + 10)  # Below head

                # Determine x-position to keep text within frame
                max_line_width = max(
                    [
                        cv2.getTextSize(line, font, font_scale, thickness)[0][0]
                        for line in lines
                    ]
                )
                x = int(head_pos[0])
                if x + max_line_width > frame_width:
                    x = frame_width - max_line_width  # Shift left if too far right
                if x < 0:
                    x = 0  # Ensure not off the left edge

                # Draw a background rectangle for readability
                left = x - padding
                top = y_start - text_height - padding
                right = x + max_line_width + padding
                bottom = (
                    y_start
                    + (len(lines) - 1) * (text_height + spacing)
                    + text_height
                    + padding
                )
                cv2.rectangle(
                    annotated_frame, (left, top), (right, bottom), (0, 0, 0), -1
                )  # Black background

                # Draw each line of text
                y = y_start
                for line in lines:
                    cv2.putText(
                        annotated_frame,
                        line,
                        (x, y),
                        font,
                        font_scale,
                        (0, 255, 0),
                        thickness,
                    )
                    y += text_height + spacing  # Move to next line

        return annotated_frame

    def show(self, frame, scale=3):
        height, width = frame.shape[:2]
        resized_frame = cv2.resize(frame, (width * scale, height * scale))
        cv2.namedWindow("Frame", cv2.WINDOW_NORMAL)
        cv2.moveWindow("Frame", 0, 0)
        cv2.imshow("Frame", resized_frame)
