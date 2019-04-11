from datetime import datetime, timedelta

from main.models import Visit

START_WORK_H = 8
START_WORK_M = 0

END_WORK_H = 17
END_WORK_M = 0

BREAK_START_H = 12
BREAK_START_M = 0

BREAK_FINISH_H = 13
BREAK_FINISH_M = 0

VISIT_DURATION = 30  # in minutes


def create_visit_for_doctor(doctor, date):
    start_work = datetime(year=date.year, month=date.month, day=date.day, hour=START_WORK_H, minute=START_WORK_M)
    end_work = datetime(year=date.year, month=date.month, day=date.day, hour=END_WORK_H, minute=END_WORK_M)
    start_break = datetime(year=date.year, month=date.month, day=date.day, hour=BREAK_START_H, minute=BREAK_START_M)
    end_break = datetime(year=date.year, month=date.month, day=date.day, hour=BREAK_FINISH_H, minute=BREAK_FINISH_M)

    start_visit = start_work
    while start_visit < end_work:
        end_visit = start_visit + timedelta(minutes=VISIT_DURATION)
        if start_break < end_visit < end_break or start_break < start_visit < end_break:
            start_visit += timedelta(minutes=VISIT_DURATION)
            continue
        Visit.objects.create(start_date=start_visit, end_date=end_visit, doctor=doctor)
        start_visit += timedelta(minutes=VISIT_DURATION)
