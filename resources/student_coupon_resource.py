from typing import Any

from dff_framework.framework.resources.base_resource import BaseResource
from dff_framework.framework.services.config import Config

from services.data_service import CouponDataService


class StudentCouponResource(BaseResource):

    def get_by_key(self, key: str) -> Any:
        pass

    def __init__(self, config: Config):
        super().__init__(config)
        self.config = config

    def get_data_service(self) -> CouponDataService:
        result = self.config.get_config("COUPON_DATA_SERVICE")
        return result

    def get_student_info(self, email):
        data_service = self.get_data_service()
        result = data_service.get_student_info(email)
        return result

    def get_free_coupon(self):
        data_service = self.get_data_service()
        result = data_service.get_free_coupon()
        return result

    def get_info(self, email):
        data_service = self.get_data_service()
        result = data_service.get_or_assign_coupon(email)
        return result


    def assign_coupon(self, email):
        """"
        student = self.get_student_info(email)
        coupon = self.get_free_coupon()
        data_service = self.get_data_service()
        result = student
        result['coupon'] = "test_coupon"
        data_service.assign_coupon(student['email'], coupon['test_coupon'])
        return result
        """
        raise NotImplementedError()



