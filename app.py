import streamlit as st
import cv2
import numpy as np
from utils import read_video, save_video
from trackers import Tracker
from team_assigner import TeamAssigner
from player_ball_assigner import PlayerBallAssigner
from camera_movement_estimator import CameraMovementEstimator
from view_transformer import ViewTransformer
from speed_and_distance_estimator import SpeedAndDistance_Estimator
import tempfile
import os
import subprocess
import time

def process_video(video_file):
    """
    Processes the uploaded video to analyze basketball game details.

    Parameters:
        video_file (UploadedFile): The uploaded video file.

    Returns:
        str: The path to the saved processed video.
    """
    # Create a temporary file to save the uploaded video
    tfile = tempfile.NamedTemporaryFile(delete=False) 
    tfile.write(video_file.read())
    tfile.close()
    
    # Read Video
    video_frames = read_video(tfile.name)
    
    # Initialize Tracker
    tracker = Tracker('models/yolov8_trained_best_model.pt')
    tracks = tracker.get_object_tracks(video_frames, read_from_stub=False)
    
    # Get object positions 
    tracker.add_position_to_tracks(tracks)
    
    # Camera movement estimator
    camera_movement_estimator = CameraMovementEstimator(video_frames[0])
    camera_movement_per_frame = camera_movement_estimator.getCameraMovement(video_frames, read_from_stub=True)
    camera_movement_estimator.add_adjust_positions_to_tracks(tracks, camera_movement_per_frame)
    
    # View Transformer
    view_transformer = ViewTransformer()
    view_transformer.add_transformed_positions_to_tracks(tracks)
    
    # Interpolate Ball Positions
    tracks["ball"] = tracker.interpolate_ball_positions(tracks["ball"])
    
    # Speed and distance estimator
    speed_and_distance_estimator = SpeedAndDistance_Estimator()
    speed_and_distance_estimator.add_speed_and_distance_to_tracks(tracks)
    
    # Assign Player Teams
    team_assigner = TeamAssigner()
    team_assigner.assign_team_color(video_frames[0], tracks['players'][0])
    
    for frame_num, player_track in enumerate(tracks['players']):
        for player_id, track in player_track.items():
            team = team_assigner.get_player_team(video_frames[frame_num], track['bbox'], player_id)
            tracks['players'][frame_num][player_id]['team'] = team 
            tracks['players'][frame_num][player_id]['team_color'] = team_assigner.team_colors[team]
    
    # Assign Ball Acquisition
    player_assigner = PlayerBallAssigner()
    team_ball_control = []
    for frame_num, player_track in enumerate(tracks['players']):
        ball_bbox = tracks['ball'][frame_num][1]['bbox'] if frame_num in tracks['ball'] and 1 in tracks['ball'][frame_num] else None
        if ball_bbox:
            assigned_player = player_assigner.assign_player_ball(player_track, ball_bbox)
            if assigned_player != -1:
                tracks['players'][frame_num][assigned_player]['has_ball'] = True
                team_ball_control.append(tracks['players'][frame_num][assigned_player]['team'])
            else:
                team_ball_control.append(team_ball_control[-1] if team_ball_control else None)
        else:
            team_ball_control.append(team_ball_control[-1] if team_ball_control else None)
    team_ball_control = np.array(team_ball_control)
    
    # Draw output 
    output_video_frames = tracker.draw_annotations(video_frames, tracks, team_ball_control)
    output_video_frames = camera_movement_estimator.draw_camera_movement(output_video_frames, camera_movement_per_frame)
    speed_and_distance_estimator.draw_metrics(output_video_frames, tracks)
    
    # Save video
    output_path = 'output_video.mp4'
    save_video(output_video_frames, output_path)
    
    return output_path

def main():
    st.title("Basketball Video Analysis")
    
    uploaded_file = st.file_uploader("Choose a video file", type=["mp4", "avi"])
    
    if uploaded_file is not None:
        st.video(uploaded_file)
        
        if st.button("Process Video"):
            with st.spinner("Processing video..."):
                output_path = process_video(uploaded_file)
            
            st.success("Video processed successfully!")
            st.video(output_path)
            
            # Provide download link
            with open(output_path, "rb") as file:
                st.download_button(
                    label="Download processed video",
                    data=file,
                    file_name="processed_video.mp4",
                    mime="video/mp4"
                )

if __name__ == '__main__'
