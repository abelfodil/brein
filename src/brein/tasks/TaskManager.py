import queue
from typing import Dict, Iterable, List
import time
import threading
from brein.utils.log import log
from brein.tasks.Task import Task, TaskStatus


class TaskManager:
    def __init__(self):
        self.tasks: Dict[str, Task] = {}
        self.task_queue = queue.PriorityQueue()

    def add_tasks(self, tasks: Iterable[Task]) -> List[int]:
        for task in tasks:
            self.tasks[task.id] = task
            self.task_queue.put((task.next_retry_time, task.id, task))
            log.info(f"Added task {task.id} (type: {task.__class__.__name__})")

    def worker(self):
        while True:
            priority, id, task = self.task_queue.get()
            if task is None:
                break

            current_time = time.time()
            if priority > current_time:
                self.task_queue.put((priority, id, task))
                self.task_queue.task_done()
                time.sleep(1)
                continue

            try:
                log.info(f"Processing task {task.id} (type: {task.__class__.__name__})")
                task.execute()
            except Exception as e:
                log.error(f"Task {task.id} failed: {str(e)}", exc_info=True)
                # Retry with exponential backoff
                if task.schedule_retry():
                    self.task_queue.put((task.next_retry_time, id, task))
                else:
                    task.update_status(TaskStatus.FAILED)
            finally:
                self.task_queue.task_done()

    def start_workers(self, num_workers: int = 4):
        for _ in range(num_workers):
            threading.Thread(target=self.worker, daemon=True).start()


task_manager = TaskManager()
