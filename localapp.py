import streamlit as st
import tempfile
import os
import cv2
import numpy as np
from utils import read_video, save_video
from trackers import Tracker
from team_assigner import TeamAssigner
from player_ball_assigner import PlayerBallAssigner
from camera_movement_estimator import CameraMovementEstimator
from view_transformer import ViewTransformer
from speed_and_distance_estimator import SpeedAndDistance_Estimator

# Define stub paths
STUB_PATH = "stubs"

# Function to process the video
def process_video(input_file, output_path, progress_bar):
    # Read Video
    video_frames = read_video(input_file)
    progress_bar.progress(10)

    # Initialize Tracker
    tracker = Tracker('models/yolov8_trained_model_best.pt')
    stub_file = os.path.join(STUB_PATH, 'tracker_stub.pkl')
    tracks = tracker.get_object_tracks(video_frames, read_from_stub=False, stub_path=stub_file)
    progress_bar.progress(20)
    
    # Get object positions
    tracker.add_position_to_tracks(tracks)
    progress_bar.progress(30)

    # Camera movement estimator
    camera_movement_estimator = CameraMovementEstimator(video_frames[0])
    camera_stub_file = os.path.join(STUB_PATH, 'camera_movement_stub.pkl')
    camera_movement_per_frame = camera_movement_estimator.getCameraMovement(video_frames, read_from_stub=True, stub_path=camera_stub_file)
    camera_movement_estimator.add_adjust_positions_to_tracks(tracks, camera_movement_per_frame)
    progress_bar.progress(40)

    # View Transformer
    view_transformer = ViewTransformer()
    view_transformer.add_transformed_positions_to_tracks(tracks)
    progress_bar.progress(50)

    # Interpolate Ball Positions
    tracks["ball"] = tracker.interpolate_ball_positions(tracks["ball"])
    progress_bar.progress(60)

    # Speed and distance estimator
    speed_and_distance_estimator = SpeedAndDistance_Estimator()
    speed_and_distance_estimator.add_speed_and_distance_to_tracks(tracks)
    progress_bar.progress(70)

    # Assign Player Teams
    team_assigner = TeamAssigner()
    team_assigner.assign_team_color(video_frames[0], tracks['players'][0])
    for frame_num, player_track in enumerate(tracks['players']):
        for player_id, track in player_track.items():
            team = team_assigner.get_player_team(video_frames[frame_num], track['bbox'], player_id)
            tracks['players'][frame_num][player_id]['team'] = team
            tracks['players'][frame_num][player_id]['team_color'] = team_assigner.team_colors[team]
    progress_bar.progress(80)

    # Assign Ball Acquisition
    player_assigner = PlayerBallAssigner()
    team_ball_control = []
    for frame_num, player_track in enumerate(tracks['players']):
        ball_bbox = tracks['ball'][frame_num][1]['bbox']
        assigned_player = player_assigner.assign_player_ball(player_track, ball_bbox)
        if assigned_player != -1:
            tracks['players'][frame_num][assigned_player]['has_ball'] = True
            team_ball_control.append(tracks['players'][frame_num][assigned_player]['team'])
        else:
            team_ball_control.append(team_ball_control[-1] if team_ball_control else None)
    team_ball_control = np.array(team_ball_control)
    progress_bar.progress(90)

    # Draw output
    output_video_frames = tracker.draw_annotations(video_frames, tracks, team_ball_control)
    output_video_frames = camera_movement_estimator.draw_camera_movement(output_video_frames, camera_movement_per_frame)
    if 'ball' in tracks:
        speed_and_distance_estimator.draw_metrics(output_video_frames, tracks)
    progress_bar.progress(95)

    # Save video
    save_video(output_video_frames, output_path)
    progress_bar.progress(100)

# Streamlit UI
def main():
    st.title("Sports Analytics and Predictions")

    # Sidebar for video upload
    st.sidebar.header("Upload Your Video")
    uploaded_file = st.sidebar.file_uploader("Choose a video file", type=["mp4", "avi", "mov"])

    if uploaded_file is not None:
        # Create a temporary file to store the uploaded video
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmpfile:
            tmpfile.write(uploaded_file.getvalue())
            temp_input_path = tmpfile.name

        st.sidebar.video(temp_input_path)

        if st.sidebar.button("Process Video"):
            progress_bar = st.progress(0)
            with st.spinner("Processing video..."):
                # Create a temporary file for the output video
                with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmpfile:
                    temp_output_path = tmpfile.name
                
                process_video(temp_input_path, temp_output_path, progress_bar)
            
            st.success("Video processed successfully!")

            # Display processed video
            st.header("Processed Video")
            
            # Create two columns
            col1, col2 = st.columns(2)
            
            with col1:
                # Display video player
                st.video(temp_output_path)
            
            with col2:
                # Display controls
                st.subheader("Video Controls")
                st.write("Use the video player controls to play, pause, and seek through the video.")
                
                # Download button for processed video
                with open(temp_output_path, "rb") as file:
                    st.download_button(
                        label="Download Processed Video",
                        data=file,
                        file_name="processed_video.mp4",
                        mime="video/mp4"
                    )

            # Clean up temporary files
            os.unlink(temp_input_path)
            os.unlink(temp_output_path)

    else:
        st.info("Upload a video file from the sidebar to get started.")

    st.warning("Note: Uploaded and processed videos are temporarily stored and will be deleted after processing.")

# Run the Streamlit app when the script is executed directly
if __name__ == "__main__":
    main()
