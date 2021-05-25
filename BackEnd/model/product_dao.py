import pymysql

from util.exception import UnauthorizedError
from util.message import UNAUTHORIZED
from util.const import END_DATE


class ProductDao:

    def get_product_list(self, connection, filters, is_count=False):
        """상품 관리 리스트

        Author:
            이서진

        Args:
            connection: 커넥션
            filters: 필터 조건
            is_count: 카운트 조건 여부

        Returns:
        """

        if filters.get("account_type") not in ["seller", "master"]:
            raise UnauthorizedError(UNAUTHORIZED, 401)

        query = "SELECT"

        if is_count is True:
            query += " Count(*) AS count"

        else:
            if filters.get("account_type") == "master":
                query += " ss.name AS seller_category,"

            query += """
                p.created_at AS created_at,
                pi.image_url AS image_url,
                ph.name AS name,
                p.product_code AS product_code,
                p.Id AS product_number,
                ph.price AS price,
                ph.discount_rate AS discount_rate,
                ph.is_sold AS is_sold,
                ph.is_displayed AS is_displayed,
                ph.discount_start_time AS discount_start_time,
                ph.discount_end_time AS discount_end_time
            """

        query += f"""
            FROM products AS p
                INNER JOIN product_images AS pi
                    ON p.Id = pi.product_id
                INNER JOIN product_histories AS ph
                    ON p.Id = ph.product_id
                INNER JOIN sellers AS s
                    ON p.seller_id = s.Id
                INNER JOIN seller_subcategories AS ss
                    ON s.seller_subcategory_id = ss.Id
                INNER JOIN seller_histories AS sh
                    ON s.Id = sh.seller_id
            WHERE ph.is_deleted = false
              AND ph.end_time = '{END_DATE}'
              AND pi.is_main = true
        """

        if filters.get("start_date") and filters.get("end_date"):
            query += " AND p.created_at BETWEEN %(start_date)s AND %(end_date)s"

        if filters.get("start_date") and filters.get("end_date") is None:
            query += " AND p.created_at > %(start_date)s"

        if filters.get("start_date") is None and filters.get("end_date"):
            query += " AND p.created_at < %(end_date)s"

        if filters.get("product_name"):
            query += " AND ph.name LIKE %(product_name)s"

        if filters.get("product_number"):
            query += " AND p.Id = %(product_number)s"

        if filters.get("product_code"):
            query += " AND p.product_code = %(product_code)s"

        if filters.get("is_sold") is not None:
            query += " AND ph.is_sold = %(is_sold)s"

        if filters.get("is_displayed") is not None:
            query += " AND ph.is_displayed = %(is_displayed)s"

        if filters.get("is_sale"):
            query += " AND NOW() BETWEEN ph.discount_start_time AND ph.discount_end_time"

        if filters.get("is_sale"):
            query += """
                AND (NOW() NOT BETWEEN ph.discount_start_time AND ph.discount_end_time
                 OR ph.discount_start_time IS NULL)"""

        if filters.get("account_type") == "seller":
            query += " AND p.seller_id = %(account_id)s"

        elif filters.get("account_type") == "master":

            if filters.get("seller_name_en"):
                query += " AND sh.english_name LIKE %(seller_name_en)s"

            if filters.get("seller_name_kr"):
                query += " AND sh.korean_name LIKE %(seller_name_kr)s"

            if filters.get("seller_category"):
                if len(filters.get("seller_category")) == 1:
                    query += " AND ss.id = %(seller_category)s"
                else:
                    query += " AND ss.id IN %(seller_category)s"

        if not is_count:
            query += " ORDER BY p.created_at DESC"
            query += " LIMIT %(offset)s, %(limit)s"

        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(query, filters)
            product_list = cursor.fetchall()
            return product_list

    def update_product_history_end_time(self, connection, data, now):
        query = f"""
            UPDATE product_histories
            SET end_time = '{now}'
            WHERE is_deleted = false
              AND product_id = %(product_id)s
              AND end_time = '{END_DATE}'
        """

        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            result = cursor.execute(query, data)
            return result

    def insert_product_history(self, connection, data, now):
        query = f"""
            INSERT INTO product_histories(
                account_id,
                product_id,
                product_subcategory_id,
                `name`,
                shipment_information,
                price,
                detail_page_html,
                discount_rate,
                discount_start_time,
                discount_end_time,
                is_sold,
                is_displayed,
                minimum_sell_quantity,
                maximum_sell_quantity,
                comment,
                start_time,
                end_time,
                is_deleted,
                manufacturer,
                manufactured_date,
                origin
                )
            SELECT account_id,
                product_id,
                product_subcategory_id,
                `name`,
                shipment_information,
                price,
                detail_page_html,
                discount_rate,
                discount_start_time,
                discount_end_time,
                %(is_sold)s,
                %(is_displayed)s,
                minimum_sell_quantity,
                maximum_sell_quantity,
                comment,
                '{now}',
                '{END_DATE}',
                is_deleted,
                manufacturer,
                manufactured_date,
                origin
            FROM product_histories
            WHERE product_id = %(product_id)s
              AND end_time = '{now}'
        """

        print(query)
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            return cursor.execute(query, data)
