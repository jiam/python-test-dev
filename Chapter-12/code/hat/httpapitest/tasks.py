import os
import shutil

from celery import shared_task
from django.core.exceptions import ObjectDoesNotExist
from httpapitest.utils import timestamp_to_datetime,get_time_stamp
from httpapitest.utils import add_test_reports
from httpapitest.runner import run_by_project, run_by_module
from httprunner.api import HttpRunner
from httprunner.logger import logger
from httpapitest.models import Project


@shared_task
def main_hrun(testset_path, report_name):
    """
    用例运行
    :param testset_path: dict or list
    :param report_name: str
    :return:
    """
    logger.setLevel('INFO')
    kwargs = {
        "failfast": False,
    }
    runner = HttpRunner(**kwargs)
    runner.run(testset_path)
    #shutil.rmtree(testset_path)
    summary = timestamp_to_datetime(runner.summary)
    report_path = add_test_reports(summary, report_name=report_name)
    os.remove(report_path)



