import pymysql


class ProductDao:

    def get_product_list(self, connection, filters, is_count=False):

        query = "SELECT"

        if is_count:
            query += " Count(*) AS count"

        elif not is_count:
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

        query += """
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
              AND ph.end_time = '9999-12-31 23:59:59'
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
                query += " AND sh.english_Name LIKE %(seller_name_en)s"

            if filters.get("seller_name_kr"):
                query += " AND sh.korean_name LIKE %(seller_name_kr)s"

            if filters.get("seller_category"):
                if len(filters.get("seller_category")) == 1:
                    query += " AND ss.id = %(seller_category)s"
                else:
                    query += " AND ss.id IN %(seller_category)s"

        query += " ORDER BY p.created_at DESC"
        query += " LIMIT %(offset)s, %(limit)s"

        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(query, filters)
            product_list = cursor.fetchall()
            return product_list
