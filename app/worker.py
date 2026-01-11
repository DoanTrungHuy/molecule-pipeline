import os
import threading
from app.queue import task_queue
from app.run_store import run_store
from app.pipeline.runner import PipelineRunner


def worker_loop():
    while True:
        try:
            run_id = task_queue.get()
            run_store.update_status(run_id, "running")

            config = run_store.get(run_id)["config"]

            results = PipelineRunner().run(config, run_id)

            run_store.finish(run_id, results)
            
        except Exception as e:
            print(f"Worker encountered an error: {e}")


def start_worker(num_workers: int | None = None):
    if num_workers is None:
        num_workers = int(os.getenv("WORKER_THREADS", "10"))

    threads = []
    for i in range(num_workers):
        t = threading.Thread(target=worker_loop, daemon=True, name=f"worker-{i+1}")
        t.start()
        threads.append(t)

    return threads
