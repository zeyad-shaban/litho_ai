from control_msgs.action import FollowJointTrajectory
from control_msgs.msg import JointTolerance
from scara_brain.constants import MOVEMENT_DURATION
from scara_brain.constants import JOINT_NAMES
from scara_brain.utils.arm_movement import build_goal


class Station:
    joint_names: list[str] = ['column1_carriage1_joint', 'carriage1_shoulder_joint', 'shoulder_elbow_joint']
    movement_duration=1
    
    def __init__(self, name: str, mid_height: float, pick_height: float, pos_shoulder: float, pos_elbow: float, running_time: float):
        self.name = name
        self.mid_height = mid_height
        self.pick_height = pick_height
        self.pos_shoulder = pos_shoulder
        self.pos_elbow = pos_elbow
        self.running_time = running_time
        
        
    def get_traj_gnd_height(self):
        positions = [self.pick_height, self.pos_shoulder, self.pos_elbow]
        return build_goal(JOINT_NAMES, positions, duration_sec=MOVEMENT_DURATION)

    def get_traj_mid_height(self):
        positions = [self.mid_height, self.pos_shoulder, self.pos_elbow]
        return build_goal(JOINT_NAMES, positions, duration_sec=MOVEMENT_DURATION)