# Copyright 2024 Donald F. Ferguson
#
# A simple service factory for wiring together the resource implementations and services for
# the microservice/web application.
#
from abc import ABC

from dff_framework.framework.services.service_factory import BaseServiceFactory
from dff_framework.framework.services.config import Config
from services.data_service import CouponDataService
from resources.student_coupon_resource import StudentCouponResource


class CouponServiceFactory(BaseServiceFactory, ABC):
    """
    A simple service factory.
    """

    def __init__(self, config: Config = None):
        super().__init__()
        self.config = config

        if self.config is None:
            self.config = Config()

        self.create_coupon_data_service()
        self.create_coupon_service()

    def create_coupon_data_service(self):
        data_service = CouponDataService(self.config)
        self.config.set_config("COUPON_DATA_SERVICE", data_service)

    def create_coupon_service(self):
        coupon_service = StudentCouponResource(self.config)
        self.config.set_config("COUPON_RESOURCE", coupon_service)

    def get_service(self, service_name):
        """
        Get a service by name. This simply gets it out of the config.

        :param service_name: The name of the service.
        :return: The service.
        """
        result = self.config.get_config(service_name)
        return result






