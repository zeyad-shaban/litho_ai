#!/usr/bin/env python3
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    debug_autofocus = LaunchConfiguration('debug_autofocus', default='false')

    autofocus_node = Node(
        package='litho_brain',
        executable='autofocus_node',
        output='screen',
        parameters=[{'debug_autofocus': debug_autofocus}]
    )

    brain_node = Node(
        package='litho_brain',
        executable='litho_brain',
        output='screen',
    )

    return LaunchDescription([
        DeclareLaunchArgument('debug_autofocus', default_value='false',
                              description='Show autofocus debug window'),
        autofocus_node,
        brain_node,
    ])