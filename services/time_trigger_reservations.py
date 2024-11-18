import azure.functions as func
import logging
from crud.reservation import *
from models.reservation import Status
from datetime import datetime, timedelta


bp_time_trigger = func.Blueprint()

@bp_time_trigger.timer_trigger(schedule="0 */10 * * * *", arg_name="myTimer", run_on_startup=False,
              use_monitor=False) 
def timer_trigger(myTimer: func.TimerRequest) -> None:
    if myTimer.past_due:
        logging.info('The timer is past due!')
    reservations = get_reservations_by_status(Status.PENDING)
    for reservation in reservations:
        if reservation.created_at + timedelta(minutes=10) < datetime.now():
            delete_reservation(reservation.id)
    logging.info('Python timer trigger function executed.')