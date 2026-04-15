#!/usr/bin/env python3
"""Map sensor_msgs/Joy (e.g. PS4 via joy_node) to /cmd_vel for manual driving."""

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Joy


class PS4Teleop(Node):
    def __init__(self):
        super().__init__('ps4_teleop')
        self.pub = self.create_publisher(Twist, '/cmd_vel', 10)

        self.linear_axis = self.declare_parameter('linear_axis', 1).get_parameter_value().integer_value
        self.angular_axis = self.declare_parameter('angular_axis', 0).get_parameter_value().integer_value
        self.linear_scale = self.declare_parameter('linear_scale', 0.5).get_parameter_value().double_value
        self.angular_scale = self.declare_parameter('angular_scale', 1.0).get_parameter_value().double_value
        self.linear_invert = self.declare_parameter('linear_invert', -1.0).get_parameter_value().double_value
        self.angular_invert = self.declare_parameter('angular_invert', 1.0).get_parameter_value().double_value

        self.require_enable = self.declare_parameter('require_enable_button', False).get_parameter_value().bool_value
        self.enable_button = self.declare_parameter('enable_button', 4).get_parameter_value().integer_value

        self.create_subscription(Joy, '/joy', self._joy_cb, 10)

    def _axis(self, msg: Joy, index: int) -> float:
        if index < 0 or index >= len(msg.axes):
            return 0.0
        return float(msg.axes[index])

    def _joy_cb(self, msg: Joy):
        if self.require_enable:
            if self.enable_button < 0 or self.enable_button >= len(msg.buttons):
                return
            if msg.buttons[self.enable_button] == 0:
                twist = Twist()
                self.pub.publish(twist)
                return

        twist = Twist()
        twist.linear.x = self.linear_invert * self.linear_scale * self._axis(msg, self.linear_axis)
        twist.angular.z = self.angular_invert * self.angular_scale * self._axis(msg, self.angular_axis)
        self.pub.publish(twist)


def main(args=None):
    rclpy.init(args=args)
    node = PS4Teleop()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
