from header import Process, process_state, schedule_type, ScheduleQueue, schedule_type


def compare_SJF(process1, process2):
    if(process1.burst_time == process2.burst_time):
        return process1.arrival_time < process2.arrival_time
    return process1.burst_time < process2.burst_time

def compare_SRTN(process1, process2):
    if(process1.remaining_time == process2.remaining_time):
        return process1.arrival_time < process2.arrival_time
    return process1.remaining_time < process2.remaining_time

def find_process_SJF (processes):
    if(len(processes) == 0):
        return None
    result = processes[0]
    for process in processes:
        if compare_SJF(process, result):
            result = process
    return result

def find_process_SRTN (processes):
    if(len(processes) == 0):
        return None
    result = processes[0]
    for process in processes:
        if compare_SRTN(process, result):
            result = process
    return result

def SJF(schedule_queue):
    pass

def SRTN(schedule_queue):
    pass