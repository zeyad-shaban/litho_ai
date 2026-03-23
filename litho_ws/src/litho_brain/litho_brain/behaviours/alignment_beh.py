from py_trees.common import Status
import rclpy
from rclpy.node import Node
import py_trees

class AutoFocusBeh(py_trees.behaviour.Behaviour):
    def __init__(self, name: str, node: Node):
        super().__init__(name)
        self.node = node
        
    def update(self) -> Status:
        return Status.RUNNING
        
    def initialise(self) -> None:
        self.node.get_logger().info(f"ok behaviour {self.name} started...")