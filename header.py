from enum import Enum

class process_state(Enum):
    NEW = "NEW"
    READY = "READY" 
    RUNNING = "RUNNING"
    WAITING = "WAITING"
    TERMINATED = "TERMINATED"

class schedule_type(Enum):
    SJF = "SJF"
    SRTN = "SRTN"

class process:
    def __init__(self):
        self.id = ""
        self.queue_name = ""          # Tên của queue mà tiến trình thuộc về
        self.arrival_time = 0           # Thời gian đến của tiến trình
        self.burst_time = 0         # Thời gian cần để hoàn thành tiến trình
        self.remaining_time = 0       # Thời gian còn lại để hoàn thành tiến trình (dùng cho SRTN)
        self.waiting_time = 0         # Thời gian chờ của tiến trình
        self.finish_time = 0          # Thời gian hoàn thành của tiến trình
        self.state = process_state.NEW

class ScheduleQueue:
    def __init__(self):
        self.name = ""
        self.processes = []
        self.type = None
        self.time_run = 0

class Scheduler:
    def __init__(self):
        self.schedule_queues = []
        self.all_processes = []
        self.current_time = 0

    def read_data(self, filename):
        try:
            with open(filename, 'r') as f:
                line = f.readline()
                num_queues = int(line.strip())
                for i in range(num_queues):
                    line = f.readline().strip()
                    queue = ScheduleQueue()
                    parts = line.split()
                    queue.name = parts[0]
                    queue.time_run = int(parts[1])
                    queue.type = schedule_type(parts[2])
                    self.schedule_queues.append(queue)
                
                while True:
                    line = f.readline()
                    if not line:
                        break
                    parts = line.strip().split()
                    process = process()
                    process.id = parts[0]
                    process.arrival_time = int(parts[1])
                    process.burst_time = int(parts[2])
                    process.queue_name = parts[3]
                    process.remaining_time = process.burst_time
                    self.all_processes.append(process)
                
        except FileNotFoundError:
            print("File not found")
        except Exception as e:
            print(f"An error occurred: {e}")






