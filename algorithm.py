from header import Process, process_state, schedule_type, ScheduleQueue, schedule_type


# def compare_SJF(process1, process2):
#     if(process1.burst_time == process2.burst_time):
#         return process1.arrival_time < process2.arrival_time
#     return process1.burst_time < process2.burst_time

# dùng cả 2
def compare_SRTN_SJF(process1, process2):
    if(process1.remaining_time == process2.remaining_time):
        return process1.arrival_time < process2.arrival_time
    return process1.remaining_time < process2.remaining_time

#dùng cả 2
def find_process_SJF_SRTN (processes):
    if(len(processes) == 0):
        return None
    result = processes[0]
    for p in processes[1:]:
        if compare_SRTN_SJF(p, result):
            result = p
    return result

# def find_process_SRTN (processes):
#     if(len(processes) == 0):
#         return None
#     result = processes[0]
#     for process in processes[1:]:
#         if compare_SRTN_SJF(process, result):
#             result = process
#     return result

