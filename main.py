from utils import save_video, read_video
from trackers import PlayerTracker,BallTracker 
from drawers import (PlayerTracksDrawer,
                     BallTracksDrawer,
                     TeamBallControlDrawer,
                     PassInterceptionDrawer,
                     CourtKeypointDrawer,
                     TacticalViewDrawer)
from team_assigner import TeamAssigner
from ball_aquisition import BallAquisitionDetector
from pass_and_interception_detector import PassAndInterceptionDetector
from court_keypoint_detector import CourtKeypointDetector
from tactical_view_converter import TacticalViewConverter
import os
import argparse

def main():
    
    
    #read video
    video_frames = read_video("input_videos/video_2.mp4")

    #initialize tracker
    player_tracker = PlayerTracker("models/player_detector.pt")
    ball_tracker = BallTracker("models/ball_detector_model.pt")
    
    ## Initialize Keypoint Detector
    court_keypoint_detector = CourtKeypointDetector("models/court_keypoint_detector.pt")
    
    #Run tracks
    player_tracks = player_tracker.get_object_tracks(video_frames, 
                                                    read_from_stub = True, 
                                                    stub_path="stubs/player_track_stubs.pkl"
                                                    )
    ball_tracks = ball_tracker.get_object_tracks(video_frames,                                                
                                                 read_from_stub= True,
                                                 stub_path="stubs/ball_track_stubs.pkl"
                                                 )
    
    ## Run KeyPoint Extractor
    court_keypoints_per_frame = court_keypoint_detector.get_court_keypoints(video_frames,
                                                                    read_from_stub=True,
                                                                    stub_path="stubs/court_key_points_stub.pkl"
                                                                    )
    
    #Remove wrong ball detections
    ball_tracks = ball_tracker.remove_wrong_detections(ball_tracks)
    #interpolate ball tracks
    ball_tracks = ball_tracker.interpolate_ball_positions(ball_tracks)
    
    # Assign Player Teams
    team_assigner = TeamAssigner()
    player_assignment = team_assigner.get_player_teams_across_frames(video_frames,
                                                                    player_tracks,
                                                                    read_from_stub=True,
                                                                    stub_path="stubs/player_assignment_stub.pkl"
                                                                    )
    # Ball Acquisition
    ball_aquisition_detector = BallAquisitionDetector()
    ball_aquisition = ball_aquisition_detector.detect_ball_possession(player_tracks, ball_tracks)

    # Detect Passes and interceptions
    pass_and_interception_detector = PassAndInterceptionDetector()
    passes = pass_and_interception_detector.detect_passes(ball_aquisition,player_assignment)
    interceptions = pass_and_interception_detector.detect_interceptions(ball_aquisition,player_assignment)
    
    #Tactical view
    tactical_view_converter = TacticalViewConverter(
        court_image_path="./images/basketball_court.png"
    )
    
    court_keypoints_per_frame = tactical_view_converter.validate_keypoints(court_keypoints_per_frame)
    tactical_player_positions = tactical_view_converter.transform_players_to_tactical_view(court_keypoints_per_frame,player_tracks)
    
    #Draw output 
    #Initialize Drawers
    player_tracks_drawer = PlayerTracksDrawer()
    ball_tracks_drawer = BallTracksDrawer()
    team_ball_control_drawer = TeamBallControlDrawer()
    pass_interception_drawer = PassInterceptionDrawer()
    Court_keypoint_drawer = CourtKeypointDrawer()
    tactical_view_drawer = TacticalViewDrawer()
        
    #Draw object Tracks
    output_video_frames = player_tracks_drawer.draw(video_frames,
                                                    player_tracks,
                                                    player_assignment,
                                                    ball_aquisition,
                                                    )
    output_video_frames = ball_tracks_drawer.draw(output_video_frames, ball_tracks)
   
    # Draw Team Ball Control
    output_video_frames = team_ball_control_drawer.draw(output_video_frames,
                                                        player_assignment,
                                                        ball_aquisition)
    #Draw Passes and Interceptions
    output_video_frames = pass_interception_drawer.draw(output_video_frames, 
                                                        passes, 
                                                        interceptions)
    
    #Draw Court Keypoints
    output_video_frames = Court_keypoint_drawer.draw(output_video_frames, court_keypoints_per_frame)
    
    # Draw Tactical View
    output_video_frames = tactical_view_drawer.draw(output_video_frames,
                                                    tactical_view_converter.court_image_path,
                                                    tactical_view_converter.width,
                                                    tactical_view_converter.height,
                                                    tactical_view_converter.key_points,
                                                    tactical_player_positions,
                                                    player_assignment,
                                                    ball_aquisition,
                                                    )
    
    #save video
    save_video(output_video_frames,"output_videos/output_video.avi")
    
if __name__ == "__main__":
    main()
    