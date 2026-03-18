import numpy as np
from control_msgs.action import FollowJointTrajectory
from control_msgs.msg import JointTolerance
from builtin_interfaces.msg import Duration
from sensor_msgs.msg import JointState
from scara_brain import constants
from trajectory_msgs.msg import JointTrajectoryPoint

SHOULDER_LEN = 0.55
ELBOW_LEN = 0.4

def compute_joint_corrections(theta1, theta2, dx, dy):
    l1 = SHOULDER_LEN
    l2 = ELBOW_LEN
    
    J = np.array([
        [-l1 * np.sin(theta1) - l2 * np.sin(theta1 + theta2), -l2 * np.sin(theta1 + theta2)],
        [l1 * np.cos(theta1) + l2 * np.cos(theta1 + theta2), l2 * np.cos(theta1 + theta2)],
    ])
    
    J_inv = np.linalg.pinv(J)
    
    dpos = np.array([dx, dy])
    dthetas = J_inv @ dpos
    
    return dthetas
    
def get_joint_pos(msg: JointState, joint_name: str):
    idx = msg.name.index(joint_name)
    return msg.position[idx]
    
def build_goal(joint_names: list[str], positions: list[float], duration_sec: int, pos_tolerance=0.01, time_tolerance=None):
    goal = FollowJointTrajectory.Goal()
    goal.trajectory.joint_names = joint_names
    
    goal.trajectory.points = [JointTrajectoryPoint(
        positions=positions,
        time_from_start=Duration(sec=duration_sec)
    )]
    
    if pos_tolerance is not None:
        goal.goal_tolerance = [JointTolerance(name=name, position=pos_tolerance) for name in joint_names]
    if time_tolerance is not None:
        goal.goal_time_tolerance = Duration(sec=time_tolerance)
    
    return goal