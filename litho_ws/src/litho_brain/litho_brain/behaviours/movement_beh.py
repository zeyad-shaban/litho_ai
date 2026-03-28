from litho_brain.constants import X_STAGE_NAME, Y_STAGE_NAME, STAGE_STABLE_TIMEOUT, STAGE_JOINT_NAMES, STAGE_Z_BOUNDS
from rclpy.action.client import ActionClient, ClientGoalHandle, GoalStatus
from control_msgs.action import FollowJointTrajectory
from litho_brain.utils.movement_utils import build_goal
from py_trees.common import Status
from rclpy.node import Node
import py_trees
from scipy.optimize import minimize_scalar
from std_msgs.msg import Float64
from sensor_msgs.msg import JointState
import threading
import time

class GoToOriginBeh(py_trees.behaviour.Behaviour):
    def __init__(self, name: str, node: Node):
        super().__init__(name)
        
        self.node = node
        self._act_client = ActionClient(self.node, FollowJointTrajectory, '/joint_trajectory_controller/follow_joint_trajectory')
        
        self._started = False
        self._moving = True
        self._failed = False
        
        self._orig_pos = [
            -0.021000,
            -0.021000,
            0.017362,
        ]
        
    def initialise(self) -> None:
        self._moving = True
        self._failed = False
        self._started = False
        self.node.get_logger().info(f"{self.name} initialized...")
        
    def update(self) -> Status:
        if not self._act_client.server_is_ready():
            self.node.get_logger().warning("Waiting for /joint_trajectory_controller/joint_trajectory action server...")
            return Status.RUNNING
        if not self._started:
            self._started = True
            self._go_to_origin()
            self.node.get_logger().info("WE STARTED TEH SEQUENCE")
            
        if self._failed:
            return Status.FAILURE
        if self._moving:
            return Status.RUNNING
            
        self.node.get_logger().info(f"returning success...")
        return Status.SUCCESS
        
    def _go_to_origin(self):
        goal = build_goal(STAGE_JOINT_NAMES, self._orig_pos, duration_sec=1, pos_tolerance=1e-6)
        res_fut = self._act_client.send_goal_async(goal)
        res_fut.add_done_callback(self._response_cb)
    
    def _response_cb(self, fut):
        self.node.get_logger().error(f"{self.name} Goal rejected")
        goal_handle: ClientGoalHandle = fut.result()
        if not goal_handle.accepted:
            self.node.get_logger().warning(f"{self.name} Goal rejected")
            self._moving = False
            self._failed = True
            return
            
        goal_handle.get_result_async().add_done_callback(self._result_cb)
        
    def _result_cb(self, fut):
        # result: FollowJointTrajectory.Result = fut.result().result
        status: GoalStatus = fut.result().status
        
        self.node.get_logger().info(f"{self.name} status: {status}")
        if status == GoalStatus.STATUS_SUCCEEDED:
            self._moving = False
            return
        else:
            self._moving = False
            self._failed = True