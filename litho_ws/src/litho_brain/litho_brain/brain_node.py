#!/usr/bin/env python3
from litho_brain.trees import litho_tree
import rclpy
from rclpy.node import Node

class BrainNode(Node):
    def __init__(self):
        super().__init__("brain_node")
        self.get_logger().info(f"brain_node Started")
        
        self.declare_parameter('hz', 10)
        hz: float = self.get_parameter('hz').value # type: ignore
        
        self.root = litho_tree.get_root(self)
        self.root.setup()
        self._tick_timer = self.create_timer(1/hz, self._tick)
        
    def _tick(self):
        self.root.tick_once()


def main(args=None):
    rclpy.init(args=args)
    node = BrainNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()