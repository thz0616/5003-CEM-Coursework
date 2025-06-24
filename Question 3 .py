import random
import threading
import time
import statistics
from tabulate import tabulate

# ---------------------------------------------------------------------------
# Utility helpers
# ---------------------------------------------------------------------------

def get_time_ns():
    """High-precision wall-clock time in nanoseconds."""
    return time.perf_counter_ns()

# ---------------------------------------------------------------------------
# Task-specific functions
# ---------------------------------------------------------------------------

IO_DELAY = 0.05  # seconds (~50 ms) – simulates I/O so multithreading helps


def generate_random_numbers():
    """Return a list of 100 random integers in [0, 10000]."""
    return [random.randint(0, 10_000) for _ in range(100)]


def random_set_task(dest, idx, delay=IO_DELAY):

    dest[idx] = generate_random_numbers()
    time.sleep(delay)  # I/O-like wait – overlaps across threads

# ---------------------------------------------------------------------------
# Experiment runners
# ---------------------------------------------------------------------------

def run_multithreaded_once():
    """Run one multithreaded round and return elapsed ns."""
    # Create a list with 3 empty spots for our results
    random_sets = [None, None, None]

    # Create and store our worker threads
    worker_threads = []
    for set_index in range(3):
        thread = threading.Thread(
            target=random_set_task,
            args=(random_sets, set_index)
        )
        worker_threads.append(thread)

    # Measure wall-clock time while the workers run
    start_time_ns = get_time_ns()

    # Start all threads
    for thread in worker_threads:
        thread.start()

    # Wait for all threads to finish
    for thread in worker_threads:
        thread.join()

    end_time_ns = get_time_ns()

    return end_time_ns - start_time_ns


def run_non_multithreaded_once():
    """Run the same workload sequentially and return elapsed ns."""
    random_sets = [None, None, None]
    start_time_ns = get_time_ns()

    # Do each task one after another (no threading)
    for set_index in range(3):
        random_set_task(random_sets, set_index)

    end_time_ns = get_time_ns()
    return end_time_ns - start_time_ns

# ---------------------------------------------------------------------------
# High-level orchestration
# ---------------------------------------------------------------------------

def run_experiments(rounds=10):
    """Run `rounds` experiment cycles and collect timing statistics."""
    multithread_times = []
    non_multithread_times = []
    time_differences = []

    for r in range(1, rounds + 1):
        # Take median of 3 samples within the round for stability
        mt_samples = [run_multithreaded_once() for _ in range(3)]
        nmt_samples = [run_non_multithreaded_once() for _ in range(3)]

        multithread_time = int(statistics.median(mt_samples))
        non_multithread_time = int(statistics.median(nmt_samples))
        difference_time = multithread_time - non_multithread_time

        multithread_times.append(multithread_time)
        non_multithread_times.append(non_multithread_time)
        time_differences.append(difference_time)

    return multithread_times, non_multithread_times, time_differences

# ---------------------------------------------------------------------------
# Pretty printing
# ---------------------------------------------------------------------------

def display_results(multithread_times, non_multithread_times, time_differences):
    rounds = len(multithread_times)

    # Round-by-round table
    round_rows = []
    for i in range(rounds):
        round_rows.append([
            i + 1,
            multithread_times[i],
            non_multithread_times[i],
            time_differences[i]
        ])

    print("Round-by-Round Performance Comparison:")
    print(
        tabulate(
            round_rows,
            headers=[
                "Round",
                "Multithreading Time (ns)",
                "Non-Multithreading Time (ns)",
                "Difference (ns)",
            ],
            tablefmt="grid",
        )
    )

    # Summary
    total_mt = sum(multithread_times)
    total_nmt = sum(non_multithread_times)
    total_diff = sum(time_differences)
    avg_mt = total_mt / rounds
    avg_nmt = total_nmt / rounds
    avg_diff = total_diff / rounds

    summary_rows = [
        ["Total Time", total_mt, total_nmt, total_diff],
        ["Average Time", avg_mt, avg_nmt, avg_diff],
    ]
    print("\nSummary of Results:")
    print(
        tabulate(
            summary_rows,
            headers=["Metric", "Multithreading (ns)", "Non-Multithreading (ns)", "Difference (ns)"],
            tablefmt="grid",
        )
    )

# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    mt_times, nmt_times, differences = run_experiments(10)
    display_results(mt_times, nmt_times, differences)