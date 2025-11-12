#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist


class RoverTwistRelay(Node):
    """
    /rover_twist（mouse_teleopの出力）を受け取り、
    /diff_drive_controller/cmd_vel_unstamped へ一定周期で再送信するノード。
    - 最新のTwistを保持して再送信（10Hz）
    - マウス操作が止まっても停止しない
    """

    def __init__(self):
        super().__init__('rover_twist_relay')

        # Publisher: DiffDriveController へ送信
        self.pub = self.create_publisher(
            Twist, '/diff_drive_controller/cmd_vel_unstamped', 10
        )

        # Subscriber: /rover_twist から受信
        self.sub = self.create_subscription(
            Twist, '/rover_twist', self.on_twist_received, 10
        )

        # 最新Twistを保持
        self.last_twist = Twist()

        # 10Hzで再送信（0.1秒周期）
        self.timer = self.create_timer(0.1, self.republish_twist)

        self.get_logger().info('✅ rover_twist_relay: active (10Hz resend enabled)')

    def on_twist_received(self, msg):
        """ /rover_twist を受信したとき呼ばれる """
        self.last_twist = msg
        self.pub.publish(msg)  # 即時反映もする
        self.get_logger().debug(
            f'Received twist: linear={msg.linear.x:.3f}, angular={msg.angular.z:.3f}'
        )

    def republish_twist(self):
        """ 最後のTwistを定期的に再送信 """
        self.pub.publish(self.last_twist)


def main():
    rclpy.init()
    node = RoverTwistRelay()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

