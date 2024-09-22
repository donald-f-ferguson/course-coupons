
from data_service import MySQLDataService


class StudentCouponResource:

    def __init__(self):
        self.my_sql_data_service = MySQLDataService()

    def get_student_info(self, email):
        result = self.my_sql_data_service.get_student_info(email)
        return result

    def get_free_coupon(self):
        result = self.my_sql_data_service.get_free_coupon()
        return result

    def assign_coupon(self, email):
        student = self.get_student_info(email)
        coupon = self.get_free_coupon()
        result = student
        result['coupon'] = "test_coupon"
        self.my_sql_data_service.assign_coupon(student['email'], coupon['test_coupon'])
        return result



