import threading
from queue import Queue
from typing import Callable


class ThreadPool:
    """
    A basic thread pool implementation with a fixed number of threads.

    Attributes:
        num_threads (int): Number of worker threads in the pool.
        tasks (Queue): A queue storing tasks to be executed by threads.
        shutdown_flag (Event): A flag indicating when the pool is shutting down.
        threads (list): A list of worker threads.
    """

    def __init__(self, num_threads: int):
        """
        Initializes the thread pool and starts worker threads.

        Args:
            num_threads (int): The number of threads to create in the pool.
        """
        self.num_threads = num_threads
        self.tasks = Queue()
        self.threads = []
        self.shutdown_flag = threading.Event()

        # Create worker threads and start them
        for _ in range(self.num_threads):
            thread = threading.Thread(target=self.worker)
            thread.start()
            self.threads.append(thread)

    def worker(self):
        """
        Worker method for each thread. Continuously looks for tasks to execute
        and runs them if available. Each thread will stop when the shutdown flag is set.
        """
        while not self.shutdown_flag.is_set():
            try:
                # Get task from queue and execute it
                task = self.tasks.get(timeout=1)
                task()
            except Queue.Empty:
                # Timeout when queue is empty, no task to process
                continue
            finally:
                self.tasks.task_done()

    def enqueue(self, task: Callable):
        """
        Enqueues a new task for execution by the thread pool.

        Args:
            task (Callable): The task (function) to be executed by a worker thread.
        """
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
            thread.join()  # Ensure all threads have finished
