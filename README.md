# ROS2 Raspberry Pi Camera Streaming - publisher and subscriber nodes

## Introduction
This project implements a real-time video streaming pipeline from a Raspberry Pi camera module to a remote visualization workstation using ROS2. The system bridges embedded hardware with robotic middleware, enabling camera feed integration into robotic applications for monitoring, perception, or autonomous navigation tasks.

## Project Overview

The implementation follows a client-server architecture where the Raspberry Pi acts as a publisher and a remote laptop serves as the subscriber:

| Step | Component | Description |
|------|-----------|-------------|
| 1 | **Hardware Setup** | Connect Sony IMX219 camera to Raspberry Pi CSI port |
| 2 | **Driver Installation** | Build and install libcamera and rpicam-apps from source |
| 3 | **Camera Verification** | Validate hardware detection and capture test images |
| 4 | **Publisher Node** | Capture frames with OpenCV, publish as ROS2 Image messages |
| 5 | **Subscriber Node** | Receive messages, convert back to OpenCV format for visualization |
| 6 | **RViz Integration** | Display live video stream in RViz with proper QoS configuration |

## Publisher Node (Raspberry Pi)

The publisher node is responsible for capturing camera frames and transmitting them as ROS2 messages. Located in `camera_publisher.py`.

## Subscriber Node (Raspberry Pi)

The subscriber node listens for incoming image messages and prepares them for display. Located in `camera_subscriber.py`.

## Communication Architecture

The system follows a publisher-subscriber pattern across two machines:

### Raspberry Pi (Publisher Side)
- **Camera Module** captures raw video frames
- **Publisher Node** (`camera_publisher.py`):
  - Reads frames using OpenCV (`cv2.VideoCapture`)
  - Converts OpenCV images to ROS2 Image messages via CvBridge
  - Publishes messages to topic `/camera/image_raw` at 10Hz

### Network Layer
- **ROS2 Middleware** handles discovery and communication
- **Topic:** `/camera/image_raw`
- **Message Type:** `sensor_msgs/msg/Image`
- **Transport:** UDP-based DDS (Data Distribution Service)
- **Requirements:** Same ROS_DOMAIN_ID on both machines

### Remote Laptop (Subscriber Side)
- **Subscriber Node** (`camera_subscriber.py`):
  - Listens to `/camera/image_raw` topic
  - Receives Image messages with matching QoS profile
  - Converts ROS2 messages back to OpenCV format
  - Logs frame dimensions for verification
- **RViz2** provides visual display:
  - Adds Image display widget
  - Subscribes to the same topic
  - Renders live video stream in GUI

### Data Flow Summary
1. Camera captures frame → OpenCV (BGR format)
2. Publisher converts to ROS Image → Published to topic
3. DDS transmits data over network
4. Subscriber receives Image → Converts back to OpenCV
5. RViz displays frame → Real-time visualization

## Running the System

### On Raspberry Pi:
```bash
export ROS_DOMAIN_ID=4
export RMW_IMPLEMENTATION=rmw_fastrtps_cpp
ros2 run my_cam camera_publisher
```

### On Remote Laptop:
```bash
export ROS_DOMAIN_ID=4
export RMW_IMPLEMENTATION=rmw_fastrtps_cpp
ros2 run my_cam camera_subscriber
```

### For RViz Visualization:
```bash
rviz2
# Add Image display → Topic: /camera/image_raw
```
