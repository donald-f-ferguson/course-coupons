from typing import Any

from dff_framework.framework.resources.base_resource import BaseResource
from data_service import CouponDataService


class StudentCouponResource(BaseResource):

    def get_by_key(self, key: str) -> Any:
        pass

    def __init__(self, config):
        super().__init__(config)

    def get_data_service(self) -> CouponDataService:
        if self.config is None:
            self.config = dict()
            self.config["data_service"] = CouponDataService()

        result = self.config.get("data_service")
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



