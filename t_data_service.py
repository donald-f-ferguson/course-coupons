from data_service import CouponDataService
import json


def get_db_service():
    context = dict(user="root", password="dbuserdbuser",
                   host="localhost", port=3306)
    ds = CouponDataService(config=context)
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
    result = ds.get_or_assign_coupon('dff9@columbia.edu')
    print("t1: result = ", json.dumps(result, indent=2))
    """
    result = ds.get_or_assign_coupon('dff9@columbia.edu')
    print("t1: result = ", json.dumps(result, indent=2))
    result = ds.get_or_assign_coupon('fb7@columbia.edu')
    print("t1: result = ", json.dumps(result, indent=2))
    result = ds.get_or_assign_coupon('fb7@columbia.edu')
    print("t1: result = ", json.dumps(result, indent=2))
    """

if __name__ == "__main__":
    # t2()
    # t3()
    # t4()
    t5()

