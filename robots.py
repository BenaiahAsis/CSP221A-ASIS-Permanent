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

def log_action(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):

        logging.info(f"{self.name} starting {func.__name__}")

        result = func(self, *args, **kwargs)

        logging.info(f"{self.name} finished {func.__name__}")

        return result
    return wrapper

class DroneRobot(Robot):
    def __init__(self, name, battery=1000, max_altitude=400):
        super().__init__(name, battery)

        self.max_altitude = max_altitude
        
    @log_action
    def perform_task(self, **kwargs):
        self.use_battery(20)
        return f"{self.name} completed a flight up to {self.max_altitude}m."


class CleaningRobot(Robot):
    def __init__(self, name, battery=100, dust_capacity=500):
        super().__init__(name, battery)

        self.dust_capacity = dust_capacity

    def perform_task(self, **kwargs):
        self.use_battery(8)

        return f"{self.name} vacuumed up to {self.dust_capacity}ml of dust."

# --- Part 1.8: Mutable Class Attribute Demonstration (standalone, not part of Robot hierarchy) ---


class BuggyLogger:
    logs = []

    def add_log(self, message):
        self.logs.append(message)


class FixedLogger:
    def __init__(self):
        self.logs = []

    def add_log(self, message):
        self.logs.append(message)


def demonstrate_mutable_class_attribute_bug():
    print("--- Buggy version (shared list) ---")
    a = BuggyLogger()
    b = BuggyLogger()
    a.add_log("Robot A started")
    b.add_log("Robot B started")
    print("a.logs:", a.logs)
    print("b.logs:", b.logs)

    print("\n--- Fixed version (separate lists) ---")
    x = FixedLogger()
    y = FixedLogger()
    x.add_log("Robot X started")
    y.add_log("Robot Y started")
    print("x.logs:", x.logs)
    print("y.logs:", y.logs)

print("\n--- Mutable Class Attribute Demo ---")
demonstrate_mutable_class_attribute_bug()

def fleet_report(robots):
    for robot in robots:
        print(str(robot))

def run_task_safely(robot, **kwargs):
    try:
        result = robot.perform_task(**kwargs)
    except InsufficientBatteryError as e:
        logging.error(e)
    else:
        print(result)
    finally:
        print(f"{robot.name} battery is now at {robot.battery}%")
    
if __name__ == "__main__":
    try:
        r = Robot("test")
        print("ERROR: instantiated abstract Robot — this should be impossible")
    except TypeError as e:
        print("Correctly blocked:", e)

    d = DroneRobot("Aqua-Drone", battery=50, max_altitude=300)
    print(d.perform_task())
    print(d)

    c = CleaningRobot("Aqua-Cleaner", battery=75, dust_capacity=300)
    print(c.perform_task())
    print(c)

    print("\n--- Fleet Report ---")
    fleet_report([d, c])

    print("\n--- run_task_safely tests ---")
    run_task_safely(d)      
    
    low_battery_drone = DroneRobot("Low-Drone", battery=5, max_altitude=200)
    run_task_safely(low_battery_drone) 

    print(DroneRobot.perform_task.__name__)

    print("\n--- from_config test ---")
    config = {"name": "Config-Drone", "battery": 15}
    drone_from_config = DroneRobot.from_config(config)
    print(drone_from_config)
    print(repr(drone_from_config))