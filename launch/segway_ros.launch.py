from launch_ros.substitutions import FindPackageShare
from launch_ros.actions import Node
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory
from moveit_configs_utils import MoveItConfigsBuilder
import os

def generate_launch_description():

    hardware_interface = Node(
        package="segway",
        executable="segway_hardware_interface"
    )

    controller = Node(
        package="segway",
        executable="segway_controller"
    )

    joy_input = Node(
        package='joy',
        executable='joy_node',
        name='joy_node',
        parameters=[{
            'device': '/dev/input/js0',
            'deadzone': 0.1,
            'autorepeat_rate': 20.0,
        }]
    )

    joystick_teleop = Node(
        package='segway',
        executable='ps4_teleop'
    )

    return LaunchDescription(
        [
            hardware_interface,
            controller,
            # joy_input,
            # joystick_teleop
        ]
    )
