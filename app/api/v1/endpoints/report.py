import uuid

from fastapi import APIRouter, File, UploadFile, BackgroundTasks
from fastapi.params import Header

from app.db.report.crud import add_record, get_all_records, check_record_status, update_record
from app.db.user.crud import verify_token
from app.models.report import TipRequest
from app.services.report_service import ReportService
from app.utils.api_utils import error_response, success_response

router = APIRouter()

def do_task_in_background(task_id, file_path):
    try:
        report_service = ReportService(task_id, file_path)
        report_service.process_report()
    except Exception as e:
        print(">>>>>>> exception", str(e))
        update_record(task_id, f"Failed to analyze {str(e)}", False)

@router.get("/checkStatus")
async def check_status(token=Header(None)):
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
    user = verify_token(token)
    if not user:
        return error_response("Invalid or expired token", None)

    return success_response("Here are records", get_all_records(user['id']))


@router.post("/getTips")
async def tips(request: TipRequest, token=Header(None)):
    print(token)
    user = verify_token(token)
    if not user:
        return error_response("Invalid or expired token", None)

    tips = ReportService.get_tips(test_name=request.test_name, summary=request.summary, parameters=request.parameters)
    print(tips)
    return success_response("Here are tips", tips["tips"])
