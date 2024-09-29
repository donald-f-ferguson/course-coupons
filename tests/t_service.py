from resources.student_coupon_resource import StudentCouponResource
from dff_framework.framework.services.config import Config
from services.coupon_service_factory import CouponServiceFactory
import json


config = Config()
service_factory = CouponServiceFactory(config)

student_coupon_resource = StudentCouponResource(config)


def get_resource():
    result = service_factory.get_service("COUPON_RESOURCE")
    print("Resource = ", result)
    return result


def get_student_info(email):
    result = student_coupon_resource.get_student_info(email)
    return result


def t_get_info():
    pass


def t_get_info_2():
    pass


if __name__ == "__main__":
    get_resource()
    result = get_student_info('dff9@columbia.edu')
    print("Result = \n", json.dumps(result, indent=2))
