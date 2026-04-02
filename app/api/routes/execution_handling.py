from fastapi import APIRouter, HTTPException

from app.managers.execution_manager import ExecutionManager

router = APIRouter(prefix="/execution", tags=["Execution"])

execution_manager = ExecutionManager()


@router.post("/run/{execution_id}")
def run_execution(execution_id: str):
    try:
        return execution_manager.run_execution(execution_id)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.get("/{execution_id}")
def get_execution_status(execution_id: str):
    try:
        return execution_manager.get_execution(execution_id)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/{execution_id}/results")
def get_execution_results(execution_id: str):
    try:
        return execution_manager.get_execution_result(execution_id)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc