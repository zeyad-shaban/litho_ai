#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from std_msgs.msg import Float64
import cv2
from litho_brain.utils.cv_utils import imgmsg_to_cv2

class AutoFocusNode(Node):
    def __init__(self):
        super().__init__("auto_focus_node")
        self.get_logger().info(f"auto_focus_node Started")
        
        self.declare_parameter('debug_autofocus', True)
        self._debug_autofocus = self.get_parameter('debug_autofocus').value

        self._img_sub = self.create_subscription(Image, '/camera/image', self._img_callback, 10)
        self._sharpness_pub = self.create_publisher(Float64, 'autofocus/sharpness', 10)
        
        
    def _img_callback(self, msg: Image):
        img = imgmsg_to_cv2(msg)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        laplacian = cv2.Laplacian(gray, cv2.CV_64F)
        sharpness = laplacian.var().item()
        
        self._sharpness_pub.publish(Float64(data=sharpness))

        
        if self._debug_autofocus:
            display = cv2.normalize(laplacian, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U) # type: ignore
            cv2.putText(display, f"Sharpness: {sharpness:.2f}", (10, 30), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            cv2.imshow('autofocus_laplacian', display)
            # cv2.imshow('autofocus_camera', img)
            cv2.waitKey(1)

        

def main(args=None):
    rclpy.init(args=args)
    node = AutoFocusNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()