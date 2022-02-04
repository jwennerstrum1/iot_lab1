import picar_4wd as fc
import time

class us_module:
    def __init__(self, step_size=5, scale=1):
        self.us_step = step_size
        self.current_angle = 90
        self.scan_list = []
        self.scale = scale # distance measured in 1:1 cm by default

    def reset(self):
        self.current_angle = 90
        fc.servo.set_angle(self.current_angle)
        time.sleep(0.5)
        self.scan_list = []
        
    def scan_step(self):
        self.current_angle -= self.us_step
        distance = fc.get_distance_at(self.current_angle)
        return distance * self.scale

    def scan_horizon(self):
        self.reset()
        distance = self.scan_step()
        while self.current_angle > -90:
            self.scan_list.append((distance, self.current_angle))
            distance = self.scan_step()
        return self.scan_list
        

    
