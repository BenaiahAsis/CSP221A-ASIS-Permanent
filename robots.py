import abc
import functools
import logging

logging.basicConfig(level=logging.INFO)


class Robot(abc.ABC):
    manufacturer = "Ben Robotics"

    population = 0

    def __init__(self, name, battery=100):
        self.name = name
        self.battery = battery

        Robot.population += 1

    @property
    def battery(self):
        return self._battery

    @battery.setter
    def battery(self, value):
        self._battery = max(0, min(100, value))

    def __str__(self):
        return f"{self.name} ({self.battery}% battery)"

    def __repr__(self):
        return f"{self.__class__.__name__}(name={self.name!r}, battery={self.battery})"

    def use_battery(self, amount):
        if self.battery < amount:
            raise InsufficientBatteryError(self.name, amount, self.battery)
        self.battery -= amount

    @classmethod
    def from_config(cls, config):
        return cls(
            name=config["name"], 
            battery=config.get("battery", 100)
        )

    @abc.abstractmethod
    def perform_task(self, **kwargs):
        pass


class InsufficientBatteryError(Exception):
    def __init__(self, robot_name, required, available):
        self.robot_name = robot_name
        self.required = required
        self.available = available

        message = f"{self.robot_name} needs {self.required}% battery for this task but only has {self.available}%."

        super().__init__(message)


class DroneRobot(Robot):
    def __init__(self, name, battery=100, max_altitude=400):
        super().__init__(name, battery)

        self.max_altitude = max_altitude

    def perform_task(self, **kwargs):
        self.use_battery(20)

        return f"{self.name} completed a flight up to {self.max_altitude}m."

d = DroneRobot("Aqua-Drone", battery=50, max_altitude=300)
print(d.perform_task())
print(d)
