import sys
from enum import Enum

# định nghĩa state của process
class process_state(Enum):
    NEW = "NEW" 
    READY = "READY" 
    RUNNING = "RUNNING"
    WAITING = "WAITING"
    TERMINATED = "TERMINATED"

#loại thuật toán cho queue
class schedule_type(Enum):
    SJF = "SJF"
    SRTN = "SRTN"

#lưu thông tin cho process
class process:
    def __init__(self):
        self.id = ""
        self.queue_name = ""          # Tên của queue mà tiến trình thuộc về
        self.arrival_time = 0           # Thời gian đến của tiến trình
        self.burst_time = 0         # Thời gian cần để hoàn thành tiến trình
        self.remaining_time = 0       # Thời gian còn lại để hoàn thành tiến trình (dùng cho SRTN)
        self.waiting_time = 0         # Thời gian chờ của tiến trình
        self.finish_time = 0          # Thời gian hoàn thành của tiến trình
        self.turnaround = 0            # Thời gian hoàn thành - thời gian đến   
        self.state = process_state.NEW

#lưu thông tin cho queue
class ScheduleQueue:
    def __init__(self):
        self.name = ""
        self.processes = []
        self.type = None
        self.time_run = 0

#lưu thông tin cho tiến trình chạy trên CPU (dùng để ghi log)
class Schedule:
    def __init__(self):
        self.start_time = 0
        self.end_time = 0
        self.queue_name = ""
        self.process_id = ""

def compare_SRTN_SJF(process1, process2):
    if(process1.remaining_time == process2.remaining_time):
        return process1.arrival_time < process2.arrival_time
    return process1.remaining_time < process2.remaining_time

# Tìm process có thời gian chạy ngắn nhất trong số các process READY
def find_process_SJF_SRTN (processes):
    if(len(processes) == 0):
        return None
    ready_processes = []
    for p in processes:
        if(p.state == process_state.READY):
            ready_processes.append(p)

    if len(ready_processes) == 0:
        return None
    result = ready_processes[0]
    for process in ready_processes[1:]:
        if compare_SRTN_SJF(process, result):
            result = process
    return result

class Scheduler:
    def __init__(self):
        self.schedule_queues = []
        self.all_processes = []
        self.current_time = 0

        self.logs = []
        self.current_segment_start = -1
        self.current_segment_queue = ""
        self.current_segment_process = ""

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
                    p = process()
                    p.id = parts[0]
                    p.arrival_time = int(parts[1])
                    p.burst_time = int(parts[2])
                    p.queue_name = parts[3]
                    p.remaining_time = p.burst_time
                    self.all_processes.append(p)
                
        except FileNotFoundError:
            print("File not found")
        except Exception as e:
            print(f"An error occurred: {e}")

    def check_new_arrivals(self):
        """Kiểm tra process mới đến tại thời điểm hiện tại"""
        for p in self.all_processes:
            if p.arrival_time == self.current_time and p.state == process_state.NEW:
                p.state = process_state.READY
                # Thêm vào queue tương ứng
                for queue in self.schedule_queues:
                    if queue.name == p.queue_name:
                        queue.processes.append(p)
                        break
    
    def record_log(self, queue_name, process_id):
        """Ghi log để xuất ra output"""
        if self.current_segment_queue != queue_name or self.current_segment_process != process_id:
            # Lưu segment trước
            if self.current_segment_start != -1:
                log = Schedule()
                log.start_time = self.current_segment_start
                log.end_time = self.current_time
                log.queue_name = self.current_segment_queue
                log.process_id = self.current_segment_process
                self.logs.append(log)
            
            # Bắt đầu segment mới
            self.current_segment_start = self.current_time
            self.current_segment_queue = queue_name
            self.current_segment_process = process_id  

    def SJF(self, queue, time_run):
        if not queue.processes:
            return 0
        
        select_process = find_process_SJF_SRTN(queue.processes)
        if select_process is None:
            return 0
        
        select_process.state = process_state.RUNNING
        # time_to_run = min(time_run, select_process.burst_time)
        time_to_run = min(time_run, select_process.remaining_time)

        for _ in range(time_to_run):
            self.record_log(queue.name, select_process.id)
            self.current_time += 1
            select_process.remaining_time -= 1

            self.check_new_arrivals()  # Kiểm tra nếu có process mới đến trong lúc chạy

            if select_process.remaining_time == 0:
                select_process.state = process_state.TERMINATED
                select_process.finish_time = self.current_time
                select_process.turnaround = select_process.finish_time - select_process.arrival_time
                select_process.waiting_time = select_process.turnaround - select_process.burst_time
                queue.processes.remove(select_process)
                break
        
      
        if select_process.remaining_time > 0:
            select_process.state = process_state.READY
            
        return time_to_run
    
    def SRTN(self, queue, time_run):
        if not queue.processes:
            return 0
        time_to_run = 0

        while time_to_run < time_run:
            select_process = find_process_SJF_SRTN(queue.processes)
            if select_process is None:
                break

            select_process.state = process_state.RUNNING

            self.record_log(queue.name, select_process.id)
            self.current_time += 1
            time_to_run += 1
            select_process.remaining_time -= 1

            self.check_new_arrivals()  

            if select_process.remaining_time == 0:
                select_process.state = process_state.TERMINATED
                select_process.finish_time = self.current_time
                select_process.turnaround = select_process.finish_time - select_process.arrival_time
                select_process.waiting_time = select_process.turnaround - select_process.burst_time
                queue.processes.remove(select_process)
            else:
                select_process.state = process_state.READY
        return time_to_run
    
    def check_all_terminated(self):
        for process in self.all_processes:
            if process.state != process_state.TERMINATED:
                return False
        return True
    
    def run_round_robin(self):
        self.check_new_arrivals()
        
        while not self.check_all_terminated():
            system_idle = True
            
            # Round Robin qua từng queue
            for queue in self.schedule_queues:
                if not queue.processes:
                    continue
                
                system_idle = False
                remaining_time = queue.time_run
                
                # Chọn thuật toán phù hợp
                if queue.type == schedule_type.SJF:
                    while remaining_time > 0 and queue.processes:
                        time_used = self.SJF(queue, remaining_time)
                        remaining_time -= time_used
                        if time_used == 0:
                            break
                
                elif queue.type == schedule_type.SRTN:
                    self.SRTN(queue, remaining_time)
            
            # Nếu tất cả queue rỗng nhưng còn process chưa đến
            if system_idle:
                next_arrival = -1
                for p in self.all_processes:
                    if p.state == process_state.NEW and p.arrival_time > self.current_time:
                        if next_arrival == -1 or p.arrival_time < next_arrival:
                            next_arrival = p.arrival_time
                
                if next_arrival != -1:
                    self.current_time = next_arrival
                    self.check_new_arrivals()
                else:
                    break
        
        if self.current_segment_start != -1:
            log = Schedule()
            log.start_time = self.current_segment_start
            log.end_time = self.current_time
            log.queue_name = self.current_segment_queue
            log.process_id = self.current_segment_process
            self.logs.append(log)


    def print_output(self, output_file):
        """In kết quả ra file output"""
        try:
            with open(output_file, 'w') as f:
                # CPU SCHEDULING DIAGRAM
                f.write("=" * 20 + " CPU SCHEDULING DIAGRAM " + "=" * 20 + "\n\n")
                f.write(f"{'[Start - End]':<20} {'Queue':<16} {'Process'}\n")
                f.write("-" * 70 + "\n")
                
                for log in self.logs:
                    time_str = f"[{log.start_time} - {log.end_time}]"
                    f.write(f"{time_str:<20} {log.queue_name:<16} {log.process_id}\n")
                
                # PROCESS STATISTICS
                f.write("\n" + "=" * 16 + " PROCESS STATISTICS " + "=" * 16 + "\n\n")
                f.write(f"{'Process':<12} {'Arrival':<12} {'Burst':<12} {'Completion':<16} {'Turnaround':<16} {'Waiting'}\n")
                f.write("-" * 100 + "\n")
                
                # Sắp xếp theo ID
                sorted_processes = sorted(self.all_processes, key=lambda p: p.id)
                
                for p in sorted_processes:
                    f.write(f"{p.id:<12} {p.arrival_time:<12} {p.burst_time:<12} "
                           f"{p.finish_time:<16} {p.turnaround:<16} {p.waiting_time}\n")
                
                f.write("-" * 100 + "\n")
                
                # Tính average
                n = len(self.all_processes)
                avg_turnaround = sum(p.turnaround for p in self.all_processes) / n
                avg_waiting = sum(p.waiting_time for p in self.all_processes) / n
                
                f.write(f"\nAverage Turnaround Time : {avg_turnaround:.1f}\n")
                f.write(f"Average Waiting Time  : {avg_waiting:.1f}\n")
                f.write("\n" + "=" * 58 + "\n")
        
        except Exception as e:
            print(f"Error writing output: {e}")
    

def main():
    # Kiểm tra argument từ command line
    if len(sys.argv) != 3:
        print("Usage: 24127029.exe <input_file> <output_file>")
        print("Example: 24127029.exe input.txt output.txt")
        sys.exit(1)
        
    # Nhận từ command line
    input_file = sys.argv[1]   
    output_file = sys.argv[2]  
    
    scheduler = Scheduler()
    
    # Đọc dữ liệu
    print(f"Reading input from {input_file}...")
    scheduler.read_data(input_file)
    
    
    # Chạy scheduler
    print("Running scheduler...")
    scheduler.run_round_robin()
    
    # Ghi kết quả
    print(f"Writing output to {output_file}...")
    scheduler.print_output(output_file)
    
    print("Done!")


if __name__ == "__main__":
    main()