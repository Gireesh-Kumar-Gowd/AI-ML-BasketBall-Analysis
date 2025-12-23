from utils import save_video, read_video
from trackers import PlayerTracker,BallTracker
from drawers import PlayerTracksDrawer

def main():
    
    
    #read video
    video_frames = read_video("input_videos/video_1.mp4")

    #initialize tracker
    player_tracker = PlayerTracker("models/player_detector.pt")
    ball_tracker = BallTracker("trackers/ball_tracker.py")
    
    #Run tracks
    player_tracks = player_tracker.get_object_tracks(video_frames, 
                                              read_from_stub = True, 
                                              stub_path="stubs/player_track_stubs.pkl"
                                              )
    ball_tracks = ball_tracker.get_object_tracks(video_frames,                                                
                                                 read_from_stub= True,
                                                 stub_path="stubs/ball_track_stubs.pkl"
                                                 )
    
    #Draw output 
    #Initialize Drawers
    player_tracks_drawer = PlayerTracksDrawer()
    
    #Draw object Tracks
    output_video_frames = player_tracks_drawer.draw(video_frames, player_tracks)
    
    #save video
    save_video(output_video_frames,"output_videos/output_video.avi")
    
if __name__ == "__main__":
    main()
    