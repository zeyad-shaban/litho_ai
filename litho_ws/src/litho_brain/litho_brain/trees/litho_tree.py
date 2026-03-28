from litho_brain.behaviours.movement_beh import GoToOriginBeh
from litho_brain.behaviours.focus_beh import AutoFocusBeh
import py_trees
from py_trees.composites import Sequence, Selector, Parallel
import rclpy
from rclpy.node import Node


def get_root(node: Node):
    root = py_trees.composites.Sequence(name='lol', memory=True)
    
    root.add_child(GoToOriginBeh('GoToOrigin', node))
    root.add_child(AutoFocusBeh('Auto focus', node))
    # root.add_child(AutoAlign)
    # root.add_child(DLPExpose)
    return root