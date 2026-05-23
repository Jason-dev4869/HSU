#!/usr/bin/env python3
import rospy
import math
from std_msgs.msg import Float32
from jetracer.nvidia_racecar import NvidiaRacecar  # hoặc Waveshare equivalent

class LineController:
    def __init__(self):
        rospy.init_node('line_controller')

        # PID gains — tune dần dần!
        self.Kp = rospy.get_param('~Kp', 0.6)
        self.Ki = rospy.get_param('~Ki', 0.01)
        self.Kd = rospy.get_param('~Kd', 0.15)

        self.base_throttle = rospy.get_param('~throttle', 0.18)

        self.integral = 0.0
        self.prev_error = 0.0
        self.last_time = rospy.Time.now()
        self.last_known_error = 0.0  # nhớ error cuối khi mất line

        self.car = NvidiaRacecar()
        self.car.throttle_gain = 0.6

        rospy.Subscriber('/line/error', Float32, self.on_error)
        rospy.loginfo("Line Controller ready")

    def on_error(self, msg):
        error = msg.data

        # Mất line — giữ hướng cuối
        if math.isnan(error):
            self.car.steering = -self.last_known_error * 0.5
            self.car.throttle = self.base_throttle * 0.5
            return

        self.last_known_error = error
        now = rospy.Time.now()
        dt = (now - self.last_time).to_sec()
        if dt <= 0: dt = 0.02
        self.last_time = now

        # PID
        self.integral += error * dt
        self.integral = max(-1.0, min(1.0, self.integral))  # anti-windup

        derivative = (error - self.prev_error) / dt
        self.prev_error = error

        steering = -(self.Kp * error
                   + self.Ki * self.integral
                   + self.Kd * derivative)

        # Giảm tốc khi cua gấp
        throttle = self.base_throttle * (1.0 - 0.4 * abs(error))

        self.car.steering = max(-1.0, min(1.0, steering))
        self.car.throttle = max(0.0, throttle)

    def run(self):
        rospy.spin()
        # Dừng xe khi node tắt
        self.car.throttle = 0.0

if __name__ == '__main__':
    LineController().run()