import os

import time

from .base_page import BasePage
from .log_config import get_logger

_mylogger = get_logger(os.path.basename(__file__))
class SpecialMethods(BasePage):
    def __init__(self, driver):
        # self.driver = driver
        super().__init__(driver)