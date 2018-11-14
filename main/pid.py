
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
        derivative = (error - self._last_error) / dt

        return self.kp * error + self.ki * self._integral + self.kd * derivative

    def reset_integral(self):
        self._integral = 0