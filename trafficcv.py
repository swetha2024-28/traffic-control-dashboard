import cv2
import numpy as np
from ultralytics import YOLO
import pygame
import time
from collections import deque
import logging

# Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Pygame constants
WIDTH, HEIGHT = 1000, 800
ROAD_WIDTH = 120
FPS = 30
ROAD_COLOR = (50, 50, 50)
GRASS_COLOR = (0, 128, 0)
LINE_COLOR = (255, 255, 255)
YELLOW_COLOR = (255, 255, 0)

# Traffic signal timers
MIN_GREEN_TIME = 10
MAX_GREEN_TIME = 45
DEFAULT_GREEN_TIME = 20
VEHICLE_THRESHOLD = 3  # Threshold for green restart

# Vehicle tracking
class VehicleTracker:
    def __init__(self):
        self.tracks = {}
        self.next_id = 0
        self.max_disappeared = 5
    
    def update(self, detections):
        if len(detections) == 0:
            for track_id in list(self.tracks.keys()):
                self.tracks[track_id]['disappeared'] += 1
                if self.tracks[track_id]['disappeared'] > self.max_disappeared:
                    del self.tracks[track_id]
            return []
        
        current_centroids = []
        for detection in detections:
            x1, y1, x2, y2 = detection
            cx = (x1 + x2) // 2
            cy = (y1 + y2) // 2
            current_centroids.append((cx, cy))
        
        if len(self.tracks) == 0:
            for centroid in current_centroids:
                self.tracks[self.next_id] = {'centroid': centroid, 'disappeared': 0, 'positions': deque(maxlen=10), 'speed': 0.0}
                self.tracks[self.next_id]['positions'].append(centroid)
                self.next_id += 1
        else:
            track_ids = list(self.tracks.keys())
            for i, centroid in enumerate(current_centroids):
                if i < len(track_ids):
                    track_id = track_ids[i]
                    self.tracks[track_id]['centroid'] = centroid
                    self.tracks[track_id]['positions'].append(centroid)
                    self.tracks[track_id]['disappeared'] = 0
                    if len(self.tracks[track_id]['positions']) >= 2:
                        pos1 = self.tracks[track_id]['positions'][-2]
                        pos2 = self.tracks[track_id]['positions'][-1]
                        distance = np.sqrt((pos2[0]-pos1[0])**2 + (pos2[1]-pos1[1])**2)
                        self.tracks[track_id]['speed'] = distance * FPS / 100.0
        return list(self.tracks.values())

# Vehicle class
class Vehicle:
    def __init__(self, direction, pos, speed=2, vtype='car'):
        self.direction = direction
        self.pos = list(pos)
        self.speed = speed
        self.size = (25, 40)
        self.color = (100, 150, 255) if vtype == 'car' else (255, 100, 100)
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (*self.pos, *self.size))

# Simulator
class TwoWayTrafficSimulator:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Smart 2-Way Traffic Junction")
        self.clock = pygame.time.Clock()
        self.ns_vehicles = []
        self.sn_vehicles = []
        self.ns_green = True
        self.sn_green = False
        self.ns_queue_length = 0
        self.sn_queue_length = 0
        self.ns_avg_speed = 1.0
        self.sn_avg_speed = 1.0
        self.ns_vehicle_count = 0
        self.sn_vehicle_count = 0
        self.signal_timer = time.time()
        self.current_green_time = DEFAULT_GREEN_TIME
        self.running = True
        self.font = pygame.font.Font(None, 28)
        self.large_font = pygame.font.Font(None, 40)
        self.baseline_total_queue = 1  # Initialize baseline to avoid div by zero

    def update_traffic_data(self, ns_data, sn_data):
        self.ns_queue_length = ns_data['queue_length']
        self.ns_avg_speed = max(0.1, ns_data['avg_speed'])
        self.ns_vehicle_count = ns_data['vehicle_count']
        self.sn_queue_length = sn_data['queue_length']
        self.sn_avg_speed = max(0.1, sn_data['avg_speed'])
        self.sn_vehicle_count = sn_data['vehicle_count']
        self.update_vehicles()

    def update_vehicles(self):
        self.ns_vehicles = [Vehicle('NS', [WIDTH//2-60, 100 + i*50]) for i in range(min(8, self.ns_vehicle_count))]
        self.sn_vehicles = [Vehicle('SN', [WIDTH//2+40, HEIGHT-100 - i*50]) for i in range(min(8, self.sn_vehicle_count))]

    def calculate_optimal_timing(self):
        ns_demand = self.ns_queue_length / max(0.1, self.ns_avg_speed)
        sn_demand = self.sn_queue_length / max(0.1, self.sn_avg_speed)
        total_demand = ns_demand + sn_demand
        if total_demand > 0:
            ns_ratio = ns_demand / total_demand
            sn_ratio = sn_demand / total_demand
            if self.ns_green:
                next_green_time = MIN_GREEN_TIME + (ns_ratio * (MAX_GREEN_TIME - MIN_GREEN_TIME))
            else:
                next_green_time = MIN_GREEN_TIME + (sn_ratio * (MAX_GREEN_TIME - MIN_GREEN_TIME))
            return max(MIN_GREEN_TIME, min(MAX_GREEN_TIME, next_green_time))
        return DEFAULT_GREEN_TIME

    def update_signals(self):
        current_time = time.time()
        elapsed = current_time - self.signal_timer

        # Restart green if vehicle count in red lane exceeds threshold and green lane is below threshold
        if self.ns_green and self.sn_vehicle_count >= VEHICLE_THRESHOLD and self.ns_vehicle_count < VEHICLE_THRESHOLD:
            self.ns_green = False
            self.sn_green = True
            self.current_green_time = self.calculate_optimal_timing()
            self.signal_timer = current_time
        elif self.sn_green and self.ns_vehicle_count >= VEHICLE_THRESHOLD and self.sn_vehicle_count < VEHICLE_THRESHOLD:
            self.sn_green = False
            self.ns_green = True
            self.current_green_time = self.calculate_optimal_timing()
            self.signal_timer = current_time
        # Regular timing
        elif elapsed >= self.current_green_time:
            self.ns_green = not self.ns_green
            self.sn_green = not self.sn_green
            self.current_green_time = self.calculate_optimal_timing()
            self.signal_timer = current_time

    def draw_road_infrastructure(self):
        self.screen.fill(GRASS_COLOR)
        road_x = WIDTH//2 - ROAD_WIDTH//2
        pygame.draw.rect(self.screen, ROAD_COLOR, (road_x, 0, ROAD_WIDTH, HEIGHT))
        divider_x = WIDTH//2
        for y in range(0, HEIGHT, 40):
            pygame.draw.rect(self.screen, YELLOW_COLOR, (divider_x-2, y, 4, 20))

    def draw_traffic_lights(self):
        elapsed = time.time() - self.signal_timer
        remaining = max(0, self.current_green_time - elapsed)
        ns_light_x = WIDTH//2 - 80
        ns_light_y = HEIGHT//2 - 60
        pygame.draw.rect(self.screen, (0,0,0), (ns_light_x-15, ns_light_y-40, 30, 80))
        pygame.draw.circle(self.screen, (255,0,0) if not self.ns_green else (0,100,0), (ns_light_x, ns_light_y-20), 10)
        pygame.draw.circle(self.screen, (0,255,0) if self.ns_green else (100,0,0), (ns_light_x, ns_light_y+20), 10)
        sn_light_x = WIDTH//2 + 80
        sn_light_y = HEIGHT//2 - 60
        pygame.draw.rect(self.screen, (0,0,0), (sn_light_x-15, sn_light_y-40, 30, 80))
        pygame.draw.circle(self.screen, (255,0,0) if not self.sn_green else (0,100,0), (sn_light_x, sn_light_y-20), 10)
        pygame.draw.circle(self.screen, (0,255,0) if self.sn_green else (100,0,0), (sn_light_x, sn_light_y+20), 10)

    def draw_info_panel(self):
        panel_width, panel_height = 350, 250
        pygame.draw.rect(self.screen, (0,0,0), (WIDTH-panel_width-10, 10, panel_width, panel_height))
        title = self.large_font.render("Traffic Control Status", True, (255,255,255))
        self.screen.blit(title, (WIDTH-panel_width, 25))
        current_signal = "N→S GREEN" if self.ns_green else "S→N GREEN"
        signal_color = (0,255,0) if self.ns_green else (255,100,0)
        self.screen.blit(self.font.render(f"Current: {current_signal}", True, signal_color), (WIDTH-panel_width, 70))
        ns_text = f"N→S: Queue={self.ns_queue_length}, Vehicles={self.ns_vehicle_count}, Speed={self.ns_avg_speed:.1f}"
        sn_text = f"S→N: Queue={self.sn_queue_length}, Vehicles={self.sn_vehicle_count}, Speed={self.sn_avg_speed:.1f}"
        self.screen.blit(self.font.render(ns_text, True, (255,255,255)), (WIDTH-panel_width, 140))
        self.screen.blit(self.font.render(sn_text, True, (255,255,255)), (WIDTH-panel_width, 170))

        # Traffic reduction calculation
        total_queue = self.ns_queue_length + self.sn_queue_length
        if self.baseline_total_queue == 1:
            self.baseline_total_queue = total_queue
        reduction_percent = max(0, (self.baseline_total_queue - total_queue)/self.baseline_total_queue*100)
        self.screen.blit(self.font.render(f"Traffic Reduced: {reduction_percent:.1f}%", True, (255,255,0)), (WIDTH-panel_width, 200))

    def run_one_step(self):
        dt = self.clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return False
        self.update_signals()
        self.draw_road_infrastructure()
        for vehicle in self.ns_vehicles:
            vehicle.draw(self.screen)
        for vehicle in self.sn_vehicles:
            vehicle.draw(self.screen)
        self.draw_traffic_lights()
        self.draw_info_panel()
        pygame.display.flip()
        return self.running

    def close(self):
        pygame.quit()

# Camera processor
class DirectionalCameraProcessor:
    def __init__(self, camera_id, direction_name):
        self.camera_id = camera_id
        self.direction_name = direction_name
        self.model = YOLO("yolov8n.pt")
        self.vehicle_classes = [2,3,5,7]
        self.tracker = VehicleTracker()
        self.last_data = {'queue_length':0, 'avg_speed':1.0, 'vehicle_count':0}

    def process_frame(self, frame):
        if frame is None:
            return self.last_data
        results = self.model(frame, stream=True, verbose=False)
        detections = []
        for r in results:
            if hasattr(r,'boxes') and r.boxes is not None:
                for box in r.boxes:
                    cls = int(box.cls[0]) if hasattr(box,'cls') else None
                    conf = float(box.conf[0]) if hasattr(box,'conf') else 0
                    coords = box.xyxy[0] if hasattr(box,'xyxy') else None
                    if cls in self.vehicle_classes and coords is not None and conf>0.3:
                        x1,y1,x2,y2 = map(int, coords)
                        detections.append((x1,y1,x2,y2))
                        cv2.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),2)
        tracked = self.tracker.update(detections)
        avg_speed = np.mean([v['speed'] for v in tracked if v['speed']>0]) if tracked else 1.0
        self.last_data = {'queue_length':len(detections), 'avg_speed':max(0.1,avg_speed), 'vehicle_count':len(tracked)}
        return self.last_data

# Smart system
class Smart2WayTrafficSystem:
    def __init__(self):
        self.simulator = TwoWayTrafficSimulator()
        self.ns_processor = DirectionalCameraProcessor(0,"N→S")
        self.sn_processor = DirectionalCameraProcessor(1,"S→N")
        self.cap_ns = cv2.VideoCapture(0)
        self.cap_sn = cv2.VideoCapture(1)
        for cap in [self.cap_ns,self.cap_sn]:
            cap.set(cv2.CAP_PROP_FRAME_WIDTH,640)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT,480)
            cap.set(cv2.CAP_PROP_FPS,30)

    def run(self):
        logger.info("Starting Smart 2-Way Traffic System...")
        while self.simulator.running:
            ret_ns, frame_ns = self.cap_ns.read()
            ret_sn, frame_sn = self.cap_sn.read()
            if not ret_ns or not ret_sn:
                ns_data = {'queue_length':2, 'avg_speed':1.0, 'vehicle_count':2}
                sn_data = {'queue_length':1, 'avg_speed':1.5, 'vehicle_count':1}
            else:
                ns_data = self.ns_processor.process_frame(frame_ns)
                sn_data = self.sn_processor.process_frame(frame_sn)
            self.simulator.update_traffic_data(ns_data,sn_data)
            if not self.simulator.run_one_step():
                break
            if ret_ns and ret_sn:
                display_ns = cv2.resize(frame_ns,(400,300))
                display_sn = cv2.resize(frame_sn,(400,300))
                combined_frame = np.hstack([display_ns, display_sn])
                cv2.imshow('Traffic Cameras N→S | S→N',combined_frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        self.cleanup()

    def cleanup(self):
        logger.info("Shutting down system...")
        self.cap_ns.release()
        self.cap_sn.release()
        cv2.destroyAllWindows()
        self.simulator.close()
        logger.info("System stopped.")

# Main
if __name__=="__main__":
    try:
        system = Smart2WayTrafficSystem()
        system.run()
    except KeyboardInterrupt:
        logger.info("System interrupted by user")
    finally:
        cv2.destroyAllWindows()
        pygame.quit()
