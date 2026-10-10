import supervision as sv

class CourtKeypointDrawer:

    def __init__(self): 
        self.keypoint_color = '#ff2c2c'

    def draw(self, frames, court_keypoints):

        vertex_annotator = sv.VertexAnnotator(
            color=sv.Color.from_hex(self.keypoint_color),
            radius=8)
        
        vertex_label_annotator = sv.VertexLabelAnnotator(
            color=sv.Color.from_hex(self.keypoint_color),
            text_color=sv.Color.WHITE,
            text_scale=0.5,
            text_thickness=1
        )
        
        output_frames = []
        for index,frame in enumerate(frames):
            annotated_frame = frame.copy()

            ultralytics_keypoints = court_keypoints[index]
            keypoints = sv.KeyPoints(
                xy=ultralytics_keypoints.xy.cpu().numpy(),
                keypoint_confidence=(
                    ultralytics_keypoints.conf.cpu().numpy()
                    if ultralytics_keypoints.conf is not None
                    else None
                ),
            )
            # Draw dots
            annotated_frame = vertex_annotator.annotate(
                scene=annotated_frame,
                key_points=keypoints)
            # Draw labels
            annotated_frame = vertex_label_annotator.annotate(
                scene=annotated_frame,
                key_points=keypoints)

            output_frames.append(annotated_frame)

        return output_frames