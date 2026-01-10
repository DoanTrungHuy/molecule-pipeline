import threading


class RunStore:
    def __init__(self):
        self._runs = {}
        self._lock = threading.RLock()

    def create(self, run_id, config):
        with self._lock:
            self._runs[run_id] = {
                "status": "queued",
                "config": config.copy() if isinstance(config, dict) else config,
                "results": None,
            }

    def update_status(self, run_id, status):
        with self._lock:
            self._runs[run_id]["status"] = status

    def finish(self, run_id, results):
        with self._lock:
            self._runs[run_id]["status"] = "finished"
            self._runs[run_id]["results"] = results

    def fail(self, run_id, error):
        with self._lock:
            self._runs[run_id]["status"] = "failed"
            entry = {"error": str(error)}
            self._runs[run_id]["results"] = entry

    def get(self, run_id):
        with self._lock:
            run = self._runs.get(run_id)
            return run.copy() if isinstance(run, dict) else run


run_store = RunStore()
