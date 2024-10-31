import pytest
import time
from project.thread_pool import ThreadPool


# Helper function for testing
def complex_task(task_id: int, result: dict):
    """
    A more complex task that takes time to complete and stores the result in a shared dict.

    Args:
        task_id (int): The task identifier.
        result (dict): A shared dictionary to store the result.
    """
    time.sleep(0.2)  # Simulate a long-running task
    result[task_id] = f"Task {task_id} completed"


def test_thread_pool_execution_with_results():
    """
    Test that the thread pool can execute tasks and collect their results.
    """
    pool = ThreadPool(4)
    result = {}

    # Enqueue multiple tasks and store their results in a shared dictionary
    for i in range(8):
        pool.enqueue(lambda task_id=i: complex_task(task_id, result))  # Pass i as a default argument

    pool.dispose()

    # Ensure that all tasks were completed
    assert len(result) == 8
    for i in range(8):
        assert result[i] == f"Task {i} completed"


def test_thread_pool_thread_count():
    """
    Test that the thread pool creates the correct number of threads.
    """
    pool = ThreadPool(5)
    assert len(pool.threads) == 5
    pool.dispose()


def test_thread_pool_with_mixed_tasks():
    """
    Test that the thread pool can handle tasks of varying complexity and completion time.
    """
    pool = ThreadPool(3)
    result = {}

    # Enqueue short and long tasks
    pool.enqueue(lambda: complex_task(1, result))  # Long task
    pool.enqueue(lambda: time.sleep(0.1))  # Short task
    pool.enqueue(lambda: complex_task(2, result))  # Another long task

    pool.dispose()

    # Ensure all tasks completed
    assert 1 in result
    assert result[1] == "Task 1 completed"
    assert 2 in result
    assert result[2] == "Task 2 completed"


def test_thread_pool_multiple_threads_working():
    """
    Test that multiple threads can work simultaneously.
    """
    pool = ThreadPool(4)
    result = {}

    # Enqueue tasks that simulate working at the same time
    for i in range(4):
        pool.enqueue(lambda task_id=i: complex_task(task_id, result))  # Pass i as a default argument

    start_time = time.time()
    pool.dispose()
    end_time = time.time()

    # Ensure that tasks took roughly the expected amount of time
    assert len(result) == 4
    assert (
        end_time - start_time
    ) < 1  # Should complete in under 1 second with 4 threads
