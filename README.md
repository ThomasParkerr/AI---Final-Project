# AI---Final-Project

Below is a  Youtube video detailing how to use the Sports Prediction and Analytics Program, that implements yolov8 for object detection and tracking.

YOUTUBE VIDEO : https://youtu.be/EKQktOpgPwA

---

# Object Tracking and Detection Project

## Overview

This project utilizes YOLOv8 for object tracking and detection to analyze players' performance in videos. The application processes uploaded videos to track and detect objects, compute useful metrics about players, and generate an output video with these metrics. The web application is built using Streamlit, allowing users to upload videos, process them, and view/download the processed results.

## Features

- **Object Tracking**: Tracks and detects objects (players, ball) in the video using YOLOv8.
- **Metrics Calculation**: Computes various performance metrics about the players.
- **Video Processing**: Generates a processed video with annotations and metrics.
- **User Interface**: Simple and intuitive interface for uploading and processing videos.

## Deployment

### Local Deployment

To deploy and run the application locally:

1. **Download the Repository and Extract The files**

    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2. **Install Required Packages**

    Ensure you have `pip` installed and then install all required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

    The `requirements.txt` file should include all necessary packages like `streamlit`, `opencv-python-headless`, `numpy`, and any other dependencies used in your project.

3. **Run the Local Application**

    Execute the following command to start the Streamlit application locally:

    ```bash
    streamlit run localapp.py
    ```

4. **Access the Application**

    Open your web browser and navigate to `http://localhost:8501` to use the application.

### Online Deployment (On Computer/Laptop)

To deploy and run the application online using ngrok:

1. **Download the Repository and Extract all the files**

    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2. **Install Required Packages**

    Ensure you have `pip` installed and then install all required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. **Run the Online Application**

    Run the onlineapp.py file

4. **Access the Application Online**

    Run the deploy.py file to expose the app to the internet, click on the generated link

### Online Deployment (On Google Colab)

To deploy and run the application online using ngrok:

1. **Clone the Repository**

    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2. **Install Required Packages**

    Ensure you have `pip` installed and then install all required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. **Run the Online Application**

    Copy and paste onlineapp.py/localapp.py into a cell on Jupyter Notebook and run it

4. **Access the Application Online**

    Copy and paste deploy.py into the next cell and run it, click on the link to access the app on the web
    
## Online Deployment on Colab (Simplified)

    - Download DeploymentOnColab.ipynb
    - Upload it as a notebook file to colab
    - Run (Switch to GPU if available)


## Using the Application

1. **Upload a Video**
    - Click on the file uploader option to browse and select a video file from your local machine.

2. **Process the Video**
    - Once the video is loaded, click the "Process Video" button to start the processing.

3. **Wait for Processing**
    - The application will process the video. This may take some time depending on the length and complexity of the video. Feel free to grab a coffee or a snack while you wait.

4. **Download the Processed Video**
    - After processing is complete, download the output video which includes all accumulated metrics and annotations. The processed video will be displayed along with a download button.
  
5. **More Videos**
       - To Analyze multiple videos, Download each previously Analyzed Video before submitting another one to be analyzed

## Troubleshooting

- **Dependencies Issues**: Ensure all required packages are installed and compatible with your Python version.
- **ngrok Issues**: If using ngrok, make sure it’s properly installed and configured. Check ngrok’s documentation for troubleshooting.
- **Video Processing Delays**: The processing time can vary based on video length and complexity. Ensure your system meets the required performance specifications.


---

Replace `<repository-url>` and `<repository-directory>` with the actual URL and directory name of your repository. This README file provides a clear guide for deploying and using your application, both locally and online.
