import uuid

from app.utils.api_utils import error_response, success_response
from fastapi import APIRouter, File, UploadFile, BackgroundTasks
from fastapi.params import Header

from app.db.report.crud import add_record, get_all_records, check_record_status, update_record
from app.db.user.crud import verify_token
from app.models.report import TipRequest
from app.services.report_service import ReportService

router = APIRouter()

def do_task_in_background(task_id, file_path):
    """
    This function runs in the background to process the report.
    It updates the record status upon completion or failure.
    """
    update_record(task_id, "Analyzing...", True)
    print(">>>>>>> Starting analysis for task:", task_id)

    # Initialize ReportService and process the report
    try:
        report_service = ReportService(task_id, file_path)
        report_service.process_report()
    except Exception as e:
        print(">>>>>>> exception", str(e))
        update_record(task_id, f"Failed to analyze {str(e)}", False)

@router.get("/checkStatus")
async def check_status(token=Header(None)):
    """
    Check the status of the last analysis for the user identified by the token.
    Returns an error if no records found or if analysis is still pending.
    """
    user = verify_token(token)
    if not user:
        return error_response("Invalid or expired token", None)

    record_status = check_record_status(user['id'])
    if record_status is None:
        return success_response("No records found")
    if record_status['status'] == 'pending':
        return error_response("Analyzing is still in progress", record_status)
    else:
        return success_response("Analyzing is completed", record_status)


@router.post("/uploadReport")
async def upload_report(background_tasks: BackgroundTasks, token=Header(None), file: UploadFile = File(...)):
    """
    Upload a report file and start analysis in the background.
    Returns an error if the user is invalid or if another analysis is already in progress.
    """
    user = verify_token(token)
    if not user:
        return error_response("Invalid or expired token", None)

    # Check if already in progress
    record_status = check_record_status(user['id'])
    if record_status is not None and record_status['status'] == 'pending':
        task_id = record_status['task_id']
        return error_response("Please wait while previous job is completed", {"task_id": task_id})

    temp_path = f"temp_{file.filename}"
    with open(temp_path, "wb") as f:
        f.write(await file.read())

    # Add record in User
    task_id = str(uuid.uuid4())
    add_record(user['id'], task_id)
    background_tasks.add_task(do_task_in_background, task_id, temp_path)
    return success_response("Analyze Successfully Started", {"task_id": task_id})


@router.get("/getRecords")
async def read_all_my_records(token=Header(None)):
    """
    Retrieve all records for the user identified by the token.
    Returns an error if the user is invalid or if no records found.
    """
    user = verify_token(token)
    if not user:
        return error_response("Invalid or expired token", None)

    return success_response("Here are records", get_all_records(user['id']))


@router.post("/getTips")
async def tips(request: TipRequest, token=Header(None)):
    """
    Generate health tips based on the report section provided in the request.
    The user must be verified by the token.
    Returns an error if the user is invalid or if the request is malformed.
    """
    user = verify_token(token)
    if not user:
        return error_response("Invalid or expired token", None)

    tips = ReportService.get_tips(test_name=request.test_name, summary=request.summary, parameters=request.parameters)
    return success_response("Here are tips", tips["tips"])
