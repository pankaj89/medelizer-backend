from datetime import datetime

from app.db.client import records_table, mongo_to_dict


def update_record(task_id, summary, is_success):
    """
    Update the record in the database with the given task_id.
    If is_success is True, set status to 'done', otherwise set it to 'failed'.
    """
    if is_success:
        status = "done"
    else:
        status = "failed"

    records_table.update_one(
        {"task_id": task_id},  # filter
        {"$set": {"summary": str(summary), "status": status}}  # update
    )


def add_record(user_id, task_id):
    """
    Add a new record to the database with the given user_id and task_id.
    The date is set to the current datetime, summary is empty, and status is 'pending'.
    """
    records_table.insert_one({
        "user_id": user_id,
        "task_id": task_id,
        "date": datetime.now(),
        "summary": "",
        "status": 'pending'
    })


def check_record_status(user_id):
    """
    Check the most recent record for the given user_id.
    Returns the record as a dictionary if found, otherwise returns None.
    """
    list_of_records = list(records_table.find({
        "user_id": user_id,
    }).sort("date", -1))
    if len(list_of_records) > 0:
        return mongo_to_dict(list_of_records[0])
    return None


def get_all_records(user_id):
    """
    Get all records for the given user_id.
    Returns a list of dictionaries representing the records.
    """
    list_of_records = list(records_table.find({
        "user_id": user_id,
    }).sort("date", -1))
    return list(map(lambda item: mongo_to_dict(item), list_of_records))
