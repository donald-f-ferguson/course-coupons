from student_coupon_resource import StudentCouponResource
import json
from dff_framework.framework.services.data_access.MySQLRDBDataService import MySQLRDBDataService
from data_service import CouponDataService


student_coupon_resource = StudentCouponResource(config=None)


def get_db_service():
    context = dict(user="root", password="dbuserdbuser",
                   host="localhost", port=3306)
    data_service = CouponDataService(config=context)
    return data_service


def get_student_info(email):
    result = student_coupon_resource.get_student_info(email)
    return result


def t_get_info():
    ds = get_db_service()
    result = ds.get_or_assign_coupon('dff9@columbia.edu')
    print("t_get_info: result = ", json.dumps(result, indent=2))


def t_get_info_2():
    ds = get_db_service()
    result = ds.get_or_assign_coupon('aa5506@columbia.edu')
    print("t_get_info_2: result = ", json.dumps(result, indent=2))


if __name__ == "__main__":
   t_get_info_2()