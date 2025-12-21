class PlayerTracksDrawer:
    
    def __init__(self):
        pass
    
    def draw(self,video_frames,tracks):
        
        output_video_frames = []
        for frame_num , frame in enumerate(video_frames):
            
            frame  = frame.copy()
            player_dict = video_frames[frame_num]
            
            #draw player tracks
            for track_id, player in player_dict.items():
                
                frame = draw_ellipse(frame,player['bbox'],(0,0,225))
                output_video_frames.append(frame)
                
        return output_video_frames    