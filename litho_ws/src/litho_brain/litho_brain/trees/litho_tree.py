from litho_brain.behaviours.alignment_beh import AutoFocusBeh
import py_trees
from py_trees.composites import Sequence, Selector, Parallel
import rclpy
from rclpy.node import Node


def get_root(node: Node):
    root = py_trees.composites.Sequence(name='lol', memory=True)
    
    # for die in dies:
    root.add_child(AutoFocusBeh('Auto focus', node))
    # root.add_child(AutoAlign)
    # root.add_child(DLPExpose)
    return root