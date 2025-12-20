from utils import save_video, read_video

def main():
    
    #read video
    video_frames = read_video("input_videos/video_1.mp4")
    
    #save video
    save_video(video_frames,"output_videos/output_video.avi")
    
if __name__ == "__main__":
    main()