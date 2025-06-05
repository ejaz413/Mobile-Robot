#!/usr/bin/env python3
#
# Author: Ejaz Ahmad

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, OpaqueFunction
from launch.conditions import IfCondition, UnlessCondition
from launch.substitutions import Command, LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch_ros.substitutions import FindPackageShare

ARGUMENTS = [
    DeclareLaunchArgument('prefix', default_value='',description='Prefix for robot joints and linkd'),
    DeclareLaunchArgument('use_gazebo', default_value='false',choices=['true','false'], description='Whether to use Gazebo Simulation ')
]

def generate_launch_description():
    #define filenames
    urdf_package = 'yahboom_rosmaster_description'
    urdf_filename = 'rosmaster_x3.urdf.xacro'
    rviz_config_filename = 'yahboom_master_description.rviz'

    # Set paths to important files

    pkg_share_description = FindPackageShare(urdf_package)
    default_urdf_model_path = PathJoinSubstitution([pkg_share_description, 'urdf','robots', urdf_filename])
    default_rviz_config_path = PathJoinSubstitution([pkg_share_description, 'rviz',rviz_config_filename])

    # Launch Congfiguration Variables

    jsp_gui = LaunchConfiguration('jsp_gui')
    rviz_config_file = LaunchConfiguration('rviz_config_file')
    urdf_model = LaunchConfiguration('use_rviz')
    use_sim_time = LaunchConfiguration('use_sim_time')

    # Declare the Launch Arguments

    declare_jsp_gui_cmd = DeclareLaunchArgument(
        name='jsp_gui',
        default_value='true',
        choices=['true','false'],
        description='Flag to enable joint_state_publisher_gui')
    
    declare_rviz_config_file_cmd = DeclareLaunchArgument(
        name='rviz_config_file',
        default_value=default_rviz_config_path,
        description='Full path to the RVIZ config file to use'
    )

    declare_urdf_model_path_cmd = DeclareLaunchArgument(
        name='urdf_model',
        default_value=default_urdf_model_path,
        description='Absolute path to robot urdf file'
    )

    declare_use_rviz_cmd = DeclareLaunchArgument(
        name='use_rviz',
        default_value='true',
        description='Whether to start Rviz'
    )

    declare_use_sim_time_cmd = DeclareLaunchArgument(
        name='use_sim_time',
        default_value='false',
        description='Use simulation (Gazebo) clock if true'
    )

    robot_description_content = ParameterValue(Command([
        'xacro', ' ', urdf_model, ' ',
        'prefix:=',LaunchConfiguration('prefix'), ' ',
        'use_gazebo:=', LaunchConfiguration('use_gazebo')
    ]), value_type=str)

    # Subscribe to the joint states of the robot, and publish the 3D pose of each link
    start_robot_state_publisher_cmd = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{
            'use_sim_time': use_sim_time}],
            condition=UnlessCondition(jsp_gui)
    )

    


