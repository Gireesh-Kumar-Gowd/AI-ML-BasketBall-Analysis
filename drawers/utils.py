import cv2
import sys
sys.append("../")
from utils import get_bbox_width, get_center_of_box

def draw_ellipse(frame , bbox, color, track_id=None):
    y2 = int(bbox[3])
    x_center = get_center_of_box(bbox)
    width = get_bbox_width(bbox)
    
    cv2.ellipse(frame, 
                center = (x_center,y2),
                angle=0,
                startAngle=-45,
                endAngle=235,
                color=color,
                thickness=2,
                lineType=cv2.LINE_4
    )
    
    rectangle_width = 40
    rectangle_height=20
    x1_rect = x_center - rectangle_width//2
    x2_rect = x_center + rectangle_width//2
    y1_rect = (y2- rectangle_height//2) +15
    y2_rect = (y2+ rectangle_height//2) +15
    