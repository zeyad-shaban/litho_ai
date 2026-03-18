from std_msgs.msg import Empty
from py_trees.common import Status
from rclpy.node import Node
import py_trees
import time

class VacuumOn(py_trees.behaviour.Behaviour):
    def __init__(self, name: str, node: Node):
        super().__init__(name)
        
        self.node = node
        self._attach_pub = node.create_publisher(Empty, '/vacuum/attach', 10)
        
    def update(self) -> Status:
        self.node.get_logger().info(f"Starting {self.name}")
        self._attach_pub.publish(Empty())
        return Status.SUCCESS

class VacuumOff(py_trees.behaviour.Behaviour):
    def __init__(self, name: str, node: Node):
        super().__init__(name)
        
        self.node = node
        self._detach_pub = node.create_publisher(Empty, '/vacuum/detach', 10)
        
    def update(self) -> Status:
        self.node.get_logger().info(f"Starting {self.name}")
        self._detach_pub.publish(Empty())
        return Status.SUCCESS

        
        
        