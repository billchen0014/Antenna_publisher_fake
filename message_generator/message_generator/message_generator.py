# Copyright 2016 Open Source Robotics Foundation, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import rclpy
from rclpy.node import Node

from tracker_common_msgs.msg import AzimuthInclination


class MessageGenerator(Node):

    def __init__(self):
        super().__init__('message_generator')
        self.absolute_azimuth = 0.0
        self.absolute_inclination = 0.0
        self.global_stamp = 0
        self.publisher_ = self.create_publisher(AzimuthInclination, "AntennaTrackerInfo", 10)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

    def timer_callback(self):
        msg = AzimuthInclination()
        if self.absolute_azimuth == 359:
           self.absolute_azimuth = 0.0
        msg.azimuth = self.absolute_azimuth
        self.absolute_azimuth += 1
        msg.inclination = self.absolute_inclination
        msg.stamp.sec = 1000
        msg.stamp.nanosec = 0 
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing Az: %f\tInc: %f' % (self.absolute_azimuth,self.absolute_inclination))


def main(args=None):
    rclpy.init(args=args)

    message_generator = MessageGenerator()

    rclpy.spin(message_generator)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    message_generator.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
