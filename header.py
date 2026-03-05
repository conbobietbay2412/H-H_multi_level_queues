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
        self.current_time = 0





