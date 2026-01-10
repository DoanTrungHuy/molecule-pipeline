from fastapi import APIRouter, HTTPException
from app.models import RunRequest
from app.run_store import run_store
from app.queue import task_queue
import uuid

router = APIRouter()

@router.post("/runs")
def start_run(req: RunRequest):
    run_id = str(uuid.uuid4())

    run_store.create(
        run_id=run_id,
        config=req.dict(),
    )

    task_queue.put(run_id)

    return {
        "run_id": run_id,
        "status": "queued"
    }

@router.get("/runs/{run_id}")
def get_status(run_id: str):
    run = run_store.get(run_id)
    if not run:
        raise HTTPException(404)

    return {
        "run_id": run_id,
        "status": run["status"]
    }

@router.get("/runs/{run_id}/results")
def get_results(run_id: str):
    run = run_store.get(run_id)
    if not run:
        raise HTTPException(404)

    status = run["status"]
    if status == "finished":
        return {"results": run["results"]}

    if status == "failed":
        results = run.get("results") or {}
        return {
            "status": "failed",
            "error": results.get("error")
        }

    return {"status": status}


