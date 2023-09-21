"""
Description: This program simulates the Round Robin scheduling algorithm.
Author: https://github.com/shisotem
Date: 2023-07-29
"""
from typing import List


class Task:
    def __init__(self, name: str, arrival_time: int, cost: int):
        self.name = name
        self.arrival_time = arrival_time
        self.cost = cost
        self.progress = 0
        self.finish_time = 0
        self.status = "not in queue"  # "not in queue", "in queue", "finished"


def enqueue_task(queue: List[Task], task: Task) -> None:
    queue.append(task)


def dequeue_task(queue: List[Task]) -> Task:
    if not queue:
        return None
    return queue.pop(0)


def print_task_result(task_list: List[Task]) -> None:
    num_tasks = len(task_list)
    turnaround_times: List[int] = [task.finish_time - task.arrival_time for task in task_list]
    sum_turnaround_time = sum(turnaround_times)

    print(f"{'task_name':<10} {'arrival_time':<13} {'finish_time':<12} {'turnaround_time':<15}")
    for task, turnaround_time in zip(task_list, turnaround_times):
        print(f"{task.name:<10} {task.arrival_time:<13d} {task.finish_time:<12d} {turnaround_time:<15d}")
    print(f"\naverage_turnaround_time: {sum_turnaround_time / num_tasks:.2f}\n")


def add_arrived_tasks_to_queue(task_list: List[Task], time: int, queue: List[Task]) -> None:
    for task in task_list:
        if task.arrival_time <= time and task.status == "not in queue":
            enqueue_task(queue, task)
            task.status = "in queue"


def execute_task(current_task: Task, current_time: int, time_quantum: int, queue: List[Task], task_list: List[Task]) -> int:
    end_time = current_time + min(time_quantum, current_task.cost - current_task.progress)

    for t in range(current_time, end_time):
        current_task.progress += 1
        if current_task.cost != current_task.progress:
            print(f"{t + 1:2d}: {current_task.name}")

        add_arrived_tasks_to_queue(task_list, t + 1, queue)

    if current_task.cost == current_task.progress:
        current_task.status = "finished"
        print(f"{end_time:2d}: {current_task.name} => Fin")
        current_task.finish_time = end_time
    else:
        enqueue_task(queue, current_task)

    return end_time


def run_round_robin(task_list: List[Task], time_quantum: int) -> None:
    queue: List[Task] = []
    current_time = 0
    finished_task_count = 0
    num_tasks = len(task_list)

    task_list.sort(key=lambda x: x.arrival_time)

    print("\n\033[1m--- PROCESS ---\033[0m\n")
    while finished_task_count != num_tasks:
        add_arrived_tasks_to_queue(task_list, current_time, queue)
        current_task = dequeue_task(queue)

        if current_task is None:
            current_time += 1
            print(f"{current_time:2d}: -")
            continue

        current_time = execute_task(current_task, current_time, time_quantum, queue, task_list)
        finished_task_count = sum(1 for task in task_list if task.status == "finished")

    print("\n\033[1m--- RESULT ---\033[0m\n")
    print_task_result(task_list)


def main() -> None:
    print("\n\033[1m--- INPUT ---\033[0m\n")
    num_tasks = int(input("num_tasks:\n"))
    task_list: List[Task] = []

    print("\ntask_name arrival_time cost:")
    for _ in range(num_tasks):
        name, arrival_time, cost = input().split()
        task = Task(name, int(arrival_time), int(cost))
        task_list.append(task)

    time_quantum = int(input("\ntime_quantum:\n"))
    run_round_robin(task_list, time_quantum)


if __name__ == "__main__":
    main()