import os

from ament_index_python.packages import get_package_share_directory


from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, ExecuteProcess, SetEnvironmentVariable
from launch.launch_description_sources import PythonLaunchDescriptionSource

from launch_ros.actions import Node



def generate_launch_description():


    set_gz_path = SetEnvironmentVariable(
        name='GZ_SIM_SYSTEM_PLUGIN_PATH',
        value='/opt/ros/jazzy/lib/'
    )

    # Include the robot_state_publisher launch file, provided by our own package. Force sim time to be enabled
    # !!! MAKE SURE YOU SET THE PACKAGE NAME CORRECTLY !!!

    package_name='my_bot' #<--- CHANGE ME

    rsp = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory(package_name),'launch','rsp.launch.py'
                )]), launch_arguments={'use_sim_time': 'true'}.items()
    )

    # Include the Gazebo launch file, provided by the gazebo_ros package
    gazebo = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory('ros_gz_sim'), 'launch', 'gz_sim.launch.py')]),
                    launch_arguments={
                        'gz_args': '-r -v 4 empty.sdf'
                    }.items()
             )

    # # Run the spawner node from the gazebo_ros package. The entity name doesn't really matter if you only have a single robot.
    # spawn_entity = Node(package='gazebo_ros', executable='spawn_entity.py',
    #                     arguments=['-topic', 'robot_description',
    #                                '-entity', 'my_bot'],
    #                     output='screen')


    # Start Gazebo Sim (Ignition) instead of gazebo_ros
    # gazebo = ExecuteProcess(
    #     cmd=['gz', 'sim', '-v4', 'empty.sdf'],
    #     output='screen'
    # )

    # # Spawn entity using ros_gz_sim (not gazebo_ros)
    # spawn_entity = ExecuteProcess(
    #     cmd=[
    #         'ros2', 'run', 'ros_gz_sim', 'create',
    #         '-topic', 'robot_description',
    #         '-name', 'my_bot',
    #         '-x', '0', '-y', '0', '-z', '0.05'
    #     ],
    #     output='screen'
    # )

        # Spawn robot
    spawn_entity = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=[
            '-topic', 'robot_description',
            '-name', 'my_bot',
            '-allow_renaming', 'true',
            '-z', '0.1'
        ],
        output='screen'
    )

        # Bridge
    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=['/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock'
                    # Gazebo_Control
            '/cmd_vel@geometry_msgs/msg/Twist]gz.msgs.Twist',
            '/odom@nav_msgs/msg/Odometry[gz.msgs.Odometry',
            '/joint_states@sensor_msgs/msg/JointState[gz.msgs.Model',
            '/tf@tf2_msgs/msg/TFMessage[gz.msgs.Pose_V', ],
        output='screen'
    )

    # Bridge
    # bridge = Node(
    #     package='ros_gz_bridge',
    #     executable='parameter_bridge',
    #     arguments=['/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock'],
    #     output='screen'
    # )

    # Launch them all!
    return LaunchDescription([
        set_gz_path,
        rsp,
        gazebo,
        spawn_entity,
        bridge,
    ])
