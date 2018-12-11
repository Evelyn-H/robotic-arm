
class PID(object):
    """Simple PID controller implementation"""

    def __init__(self, kp, ki, kd):
        self.kp = kp
        self.ki = ki
        self.kd = kd

        self._last_error = 0
        self._integral = 0

    def update(self, target, current, dt):
        error = target - current

        self._integral += error * dt
        derivative = (self._last_error - error) / dt

        power = self.kp * error + self.ki * self._integral + self.kd * derivative
        # print(f"t {target}, \tc {current}, \tp {power}")
        return power

    def reset_integral(self):
        self._integral = 0
