import rclpy
#from rclpy.qos import QoSProfile, ReliabilityPolicy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2

class CameraPublisher(Node):

    def __init__(self):
        super().__init__('camera_publisher')

        #qos_profile = QoSProfile(depth=10)
        #qos_profile.reliability = ReliabilityPolicy.BEST_EFFORT

        #self.publisher_ = self.create_publisher(Image, 'camera/image_raw', qos_profile)
        self.publisher_ = self.create_publisher(Image, 'camera/image_raw', 10)


        self.bridge = CvBridge()

        # Open camera (0 = default camera)
        self.cap = cv2.VideoCapture(0)

        # Publish at 10 Hz
        self.timer = self.create_timer(0.1, self.timer_callback)

    def timer_callback(self):
        ret, frame = self.cap.read()

        if ret:
            msg = self.bridge.cv2_to_imgmsg(frame, encoding='bgr8')
            self.publisher_.publish(msg)
            self.get_logger().info('Publishing frame')

def main(args=None):
    rclpy.init(args=args)
    node = CameraPublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
