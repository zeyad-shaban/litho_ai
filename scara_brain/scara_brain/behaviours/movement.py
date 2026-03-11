import py_trees
from py_trees.common import Status
from rclpy.action.client import ActionClient, GoalStatus, ClientGoalHandle
from rclpy.logging import RcutilsLogger
from scara_brain.modules.station import Station


class MoveToStation(py_trees.behaviour.Behaviour):
    def __init__(self, name: str, station: Station, is_mid: bool, act_client: ActionClient, logger: RcutilsLogger):
        super().__init__(name)
        self._result = None
        self.station = station
        self.is_mid = is_mid
        self.act_client = act_client
        self.logger = logger
    
    def initialise(self) -> None:
        self._wait_for_act_server()
        goal = self.station.get_traj_mid_height() if self.is_mid else self.station.get_traj_gnd_height()
        
        fut = self.act_client.send_goal_async(goal)
        fut.add_done_callback(self._goal_response_cb)
        
        self.logger.info(f"Starting {self.name}")
        
    def update(self) -> Status:
        if self._result is None:
            return Status.RUNNING
        
        if self._result.status == GoalStatus.STATUS_SUCCEEDED:
            return Status.SUCCESS
        else: # Aborted, or cancelled
            return Status.FAILURE
    
    def terminate(self, new_status: Status) -> None:
        # idk what am i suppsoed to do here
        return super().terminate(new_status)
        
    def _goal_response_cb(self, fut):
        goal_handle: ClientGoalHandle = fut.result()
        
        if not goal_handle.accepted:
            self.logger.info("Goal rejected...") # todo make this a failure
            return
        
        result_fut = goal_handle.get_result_async()
        result_fut.add_done_callback(self._result_cb)
        
    def _result_cb(self, fut):
        self._result = fut.result()
        
    
    def _wait_for_act_server(self):
        while not self.act_client.wait_for_server(1):
            self.logger.info("Waiting for action client...")