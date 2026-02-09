import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from control_msgs.action import FollowJointTrajectory, GripperCommand
from trajectory_msgs.msg import JointTrajectoryPoint
from builtin_interfaces.msg import Duration
import sys
import tty
import termios
import select

GRIPPER_KEY_BINDINGS = {
    'g': 0.01,  # Open
    'h': -0.01  # Close
}

POSES = {
    '1': [0.0, 0.0, 0.0, 0.0] 
}

def get_key(settings):
    tty.setraw(sys.stdin.fileno())
    rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
    if rlist:
        key = sys.stdin.read(1)
    else:
        key = ''
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key

class SimpleArmController(Node):
    def __init__(self):
        super().__init__('simple_arm_controller')

        self.arm_joint_names = ['joint1', 'joint2', 'joint3', 'joint4']
        
        # Action Clients
        self.arm_action_client = ActionClient(self, FollowJointTrajectory, '/arm_controller/follow_joint_trajectory')
        self.gripper_action_client = ActionClient(self, GripperCommand, '/gripper_controller/gripper_cmd')

        self.settings = termios.tcgetattr(sys.stdin)
        self.timer = self.create_timer(0.1, self.run_loop)
        self.print_instructions()

    def run_loop(self):
        key = get_key(self.settings)
        if not key:
            return

        if key in GRIPPER_KEY_BINDINGS:
            self.send_gripper_goal(GRIPPER_KEY_BINDINGS[key])
        
        elif key in POSES:
            print(f"\rMoving to Home Position...")
            self.send_arm_goal(POSES[key], 2.0)
            
        elif key.lower() == 'q':
            self.destroy_node()
            rclpy.shutdown()
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.settings)
            sys.stdout.write('\nExiting...\n')
            sys.exit(0)

    def send_arm_goal(self, positions, duration_sec):
        if not self.arm_action_client.server_is_ready():
            self.get_logger().info("Arm action server not available")
            return
        
        goal = FollowJointTrajectory.Goal()
        goal.trajectory.joint_names = self.arm_joint_names
        point = JointTrajectoryPoint(
            positions=positions, 
            time_from_start=Duration(sec=int(duration_sec), nanosec=int((duration_sec % 1) * 1e9))
        )
        goal.trajectory.points.append(point)
        self.arm_action_client.send_goal_async(goal)

    def send_gripper_goal(self, position):
        if not self.gripper_action_client.server_is_ready():
            self.get_logger().info("Gripper action server not available")
            return
            
        goal = GripperCommand.Goal()
        goal.command.position = position
        goal.command.max_effort = 1.0
        self.gripper_action_client.send_goal_async(goal)

    def print_instructions(self):
        print("""
        --- Gripper & Home Controller ---
        
        Gripper Control:
           g : Open Gripper
           h : Close Gripper

        Arm Poses:
           1 : Move to Home Position
        
        q : Quit
        ---------------------------------
        """)

def main(args=None):
    rclpy.init(args=args)
    node = SimpleArmController()
    try:
        rclpy.spin(node)
    except (KeyboardInterrupt, SystemExit):
        pass
    finally:
        if rclpy.ok():
            rclpy.shutdown()

if __name__ == '__main__':
    main()
