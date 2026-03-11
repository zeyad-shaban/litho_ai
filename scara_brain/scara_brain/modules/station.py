from control_msgs.action import FollowJointTrajectory
from control_msgs.msg import JointTolerance
from trajectory_msgs.msg import JointTrajectoryPoint
from builtin_interfaces.msg import Duration


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
        return self._create_traj(self.pick_height)

    def get_traj_mid_height(self):
        return self._create_traj(self.mid_height)

    def _create_traj(self, height):
        goal = FollowJointTrajectory.Goal()
        
        goal.trajectory.joint_names = Station.joint_names
        
        goal.trajectory.points = [JointTrajectoryPoint(
            positions=[height, self.pos_shoulder, self.pos_elbow],
            time_from_start=Duration(sec=Station.movement_duration)
        )]
        
        goal.goal_tolerance = [JointTolerance(name=name, position=0.01) for name in Station.joint_names]
        # goal.goal_time_tolerance = Duration(sec=2)
        
        return goal