import json

import pymysql
import os
from dff_framework.framework.services.data_access.MySQLRDBDataService import MySQLRDBDataService


class CouponDataService(MySQLRDBDataService):

    student_table_name = "course_student_coupons.student_coupons"
    student_table_full = "course_student_coupons.student_coupons_full"
    coupon_table_name = "course_student_coupons.w4153_coupons"

    def __init__(self, config=None):
        """
        Instantiate an object.
        :param config: A dictionary containing configuration information.
        """
        super().__init__(config)
        self.conn = None
        self.config = config
        self.student_table_name = CouponDataService.student_table_name
        self.coupon_table_name = CouponDataService.coupon_table_name

    def test_connection(self):
        conn = self._get_connection()
        table_name = self.student_table_name
        sql = f"describe {table_name}"
        result = self.run_query(sql)
        return result

    def get_student_info(self, email):
        """
        Return information about a student.
        :param email: The student email as recorded in CourseWorks.
        :return: The student's information or None if not found.
        """
        student_table_full = self.student_table_full
        sql = f"select * from {student_table_full} where email=%s";
        result = self.run_query(
            query=sql,
            params=[email],
            return_results=True,
            commit=True
        )



        return result

    def get_free_coupon(self):
        """
        Query the cloud credit/coupon table and return an allocated coupon.
        :return: Coupon information.
        """

        coupon_table_name = self.coupon_table_name
        sql = f"select * from {coupon_table_name} where allocated_to is NULL limit 1;";
        result = self.run_query(sql, None, True)

        return result

    def assign_coupon(self, email, coupon_code):

        conn = None
        cursor = None
        final_result = None

        student_info_table = self.student_table_name
        coupon_table_name = self.coupon_table_name

        update_student_coupons_sql = f"""
            update {student_info_table} set coupon_code=%s 
                where email=%s
        """

        update_coupons_sql = f"""
            update {coupon_table_name} set allocated_to=%s 
                where coupon_code=%s
        """

        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            res1 = 0
            res2 = 0

            res1 = self.run_query(
                query=update_student_coupons_sql,
                params=[coupon_code, email],
                return_results=False,
                commit=False,
                connection=conn,
                cursor=cursor
            )

            if res1:
                res2 = self.run_query(
                    query=update_coupons_sql,
                    params=[email, coupon_code],
                    return_results=False,
                    commit=True,
                    connection=conn,
                    cursor=cursor
                )

            final_result = res1 + res2

        except Exception as e:
            print("assign_coupon Exception = ", e)
            conn.rollback()
            final_result = None

        return final_result

    def get_or_assign_coupon(self, email):
        """
        If the user identified by the email is already allocated a coupon, return the value. Otherwise,
        assign a coupon and return the value.
        :param email:
        :return:
        """

        student_info = self.get_student_info(email)
        if student_info:
            student_info = student_info[0]

        if student_info['coupon_code']:
            final_result = student_info
        else:
            free_coupon = self.get_free_coupon()
            if free_coupon:
                free_coupon = free_coupon[0]

            self.assign_coupon(email, free_coupon['coupon_code'])

            final_result = self.get_student_info(email)

        print("get_or_assign_coupon: final_result = ", json.dumps(final_result, indent=2, default=str))

        return final_result
