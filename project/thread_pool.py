import threading
from queue import Queue, Empty
from typing import Callable, List, Any


class ThreadPool:
    """
    A basic thread pool implementation with a fixed number of threads.

    Attributes:
        num_threads (int): Number of worker threads in the pool.
        tasks (Queue[Callable[[], Any]]): A queue storing tasks to be executed by threads.
        threads (list): A list of worker threads.
        shutdown_flag (Event): A flag indicating when the pool is shutting down.
    """

    def __init__(self, num_threads: int):
        self.num_threads = num_threads
        self.tasks: Queue[Callable[[], Any]] = Queue()
        self.threads: List[threading.Thread] = []
        self.shutdown_flag = threading.Event()

        # Create worker threads and start them
        for _ in range(self.num_threads):
            thread = threading.Thread(target=self.worker)
            thread.start()
            self.threads.append(thread)

    def worker(self):
        while not self.shutdown_flag.is_set() or not self.tasks.empty():
            try:
                # Get task from queue and execute it
                task = self.tasks.get(timeout=1)
                try:
                    task()  # Call the task function
                finally:
                    self.tasks.task_done()
            except Empty:
                continue

    def enqueue(self, task: Callable[[], Any]) -> None:
        """
        Enqueues a new task for execution by the thread pool.

        Args:
            task (Callable[[], Any]): The task (function) to be executed by a worker thread.
        """
        if self.shutdown_flag.is_set():
            raise RuntimeError("Cannot enqueue task after shutdown.")
        self.tasks.put(task)

    def dispose(self):
        """
        Gracefully shuts down the thread pool, waiting for all threads to finish.
        No new tasks will be accepted, and all current tasks will be completed
        before shutting down.
        """
        self.shutdown_flag.set()
        self.tasks.join()  # Wait for all tasks to complete
        for thread in self.threads:
            thread.join()
