from dff_framework.framework.services.config import Config
from services.data_service import CouponDataService
from services.coupon_service_factory import CouponServiceFactory
import json

config = Config()
service_factory = CouponServiceFactory(config)


def get_db_service():
    ds = service_factory.get_service("COUPON_DATA_SERVICE")
    result = ds.test_connection()
    print("Connection test = \n", json.dumps(result, indent=2, default=str))
    return ds


def t2():
    ds = get_db_service()
    result = ds.get_student_info('dff9@columbia.edu')
    print("t2: result = ", json.dumps(result, indent=2))
    result = ds.get_student_info('ab5666@columbia.edu')
    print("t2: result = ", json.dumps(result, indent=2))


def t3():
    ds = get_db_service()
    result = ds.get_free_coupon()
    print("t3: result = ", json.dumps(result, indent=2))


def t4():
    ds = get_db_service()
    result = ds.assign_coupon('dff9@columbia.edu', '00T8-5XJ1-4HRD-VJWD')
    print("t4: result = ", result)


def t5():
    ds = get_db_service()
    result = ds.get_or_assign_coupon('dff9@columbia.edu')
    print("t5: result = ", json.dumps(result, indent=2))
    result = ds.get_or_assign_coupon('ashesh.amatya@columbia.edu')
    print("t5: result = ", json.dumps(result, indent=2))

def t1():
    ds = get_db_service()
    """
    result = ds.get_or_assign_coupon('dff9@columbia.edu')
    print("t1: result = ", json.dumps(result, indent=2))
    result = ds.get_or_assign_coupon('fb7@columbia.edu')
    print("t1: result = ", json.dumps(result, indent=2))
    result = ds.get_or_assign_coupon('fb7@columbia.edu')
    print("t1: result = ", json.dumps(result, indent=2))
    """


if __name__ == "__main__":
    db = get_db_service()
    print("The DB service is:", db)
    # t2()
    t3()
    # t4()
    # t5()

