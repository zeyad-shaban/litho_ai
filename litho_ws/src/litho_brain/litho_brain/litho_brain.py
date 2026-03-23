#!/usr/bin/env python3
from litho_brain.trees import litho_tree
import rclpy
from rclpy.node import Node

class LithoBrain(Node):
    def __init__(self):
        super().__init__("litho_brain")
        self.get_logger().info(f"litho_brain Started")
        
        root = litho_tree.get_root(self)
        root.setup()


def main(args=None):
    rclpy.init(args=args)
    node = LithoBrain()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()