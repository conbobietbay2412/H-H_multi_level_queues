from header import Process, process_state, schedule_type, ScheduleQueue, schedule_type


def compare_SJF(process1, process2):
    if(process1.burst_time == process2.burst_time):
        return process1.arrival_time < process2.arrival_time
    return process1.burst_time < process2.burst_time

def compare_SRTN(process1, process2):
    if(process1.remaining_time == process2.remaining_time):
        return process1.arrival_time < process2.arrival_time
    return process1.remaining_time < process2.remaining_time

def SJF (processes):
    pass
