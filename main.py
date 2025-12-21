from utils import save_video, read_video
from trackers import PlayerTracker

def main():
    
    
    #read video
    video_frames = read_video("input_videos/video_1.mp4")

    #initialize tracker
    player_tracker = PlayerTracker("models/player_detector.pt")
    
    #Run tracks
    tracks = player_tracker.get_object_tracks(video_frames)
        
    #save video
    save_video(video_frames,"output_videos/output_video.avi")
    
if __name__ == "__main__":
    main()
    