from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, ExecuteProcess
from launch.substitutions import LaunchConfiguration, Command
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    pkg_share = get_package_share_directory('megarover_description')

    # URDF + Gazeboプラグインを含むモデル
    default_model_path = os.path.join(pkg_share, 'urdf', 'mega3.xacro')
    model_arg = DeclareLaunchArgument(
        name='model', default_value=str(default_model_path),
        description='Path to the robot xacro file'
    )

    robot_description = ParameterValue(
        Command(['xacro ', LaunchConfiguration('model')]),
        value_type=str
    )

    # Gazebo起動
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory('gazebo_ros'), 'launch', 'gazebo.launch.py')
        )
    )

    # robot_state_publisher
    rsp = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'robot_description': robot_description}],
        output='screen'
    )

    # Gazeboにロボットをスポーン
    spawn = ExecuteProcess(
        cmd=['ros2', 'run', 'gazebo_ros', 'spawn_entity.py',
             '-entity', 'megarover3',
             '-topic', 'robot_description'],
        output='screen'
    )

    return LaunchDescription([
        model_arg,
        gazebo,
        rsp,
        spawn
    ])

