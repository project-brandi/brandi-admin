import pymysql

from util.const import (SHIPMENT_STATUS_BEFORE_DELIVERY, 
                        ORDER_STATUS_ORDER_COMPLETED,
                        SHIPPING)

class ProductPrepareDao:
    def get_product_prepare(self, connection, filter):
        query = f"""
            SELECT 
                o.created_at, 
                o.id as order_id, 
                op.id as order_product_id, 
                sh.korean_name AS seller_name, 
                ph.`name` AS product_name,
                c.color, 
                sz.size, 
                po.extra_price, 
                oph.quantity, 
                oh.`name`, 
                oh.phone_number, 
                oph.price, 
                ss.shipment_status
            FROM orders AS o
                INNER JOIN order_products AS op
                    ON o.id = op.order_id   
                INNER JOIN products AS p
                    ON op.product_id = p.id
                INNER JOIN order_histories AS oh 
                    ON o.id = oh.order_id
                INNER JOIN order_product_histories AS oph
                    ON op.id = oph.order_product_id 
                INNER JOIN product_histories AS ph
                    ON p.id = ph.product_id
                INNER JOIN seller_histories AS sh 
                    ON p.seller_id = sh.seller_id 
                INNER JOIN sellers AS s
                    ON sh.seller_id = s.id
                INNER JOIN shipments AS sm 
                    ON op.id = sm.order_product_id
                INNER JOIN product_options AS po 
                    ON op.product_option_id = po.id
                INNER JOIN sizes AS sz 
                    ON po.size_id = sz.id
                INNER JOIN colors AS c 
                    ON po.color_id = c.id
                INNER JOIN shipment_status AS ss 
                    ON sm.shipment_status_id = ss.id
            WHERE 
                sm.shipment_status_id = {SHIPMENT_STATUS_BEFORE_DELIVERY}
                AND o.created_at >= %(start_date)s
                AND o.created_at <= %(end_date)s      
                """

        if filter.get('order_number'): 
            query += " AND o.id LIKE %(order_number)s"

        if filter.get('order_detail_number'):
            query += " AND op.id LIKE %(order_detail_number)s"
        
        if filter.get('order_name'):
            query += " AND oh.`name` LIKE %(order_name)s"

        if filter.get('order_phone'):
            query += " AND oh.phone_number LIKE %(order_phone)s"

        if filter.get('seller_name'):
            query += " AND sh.korean_name LIKE %(seller_name)s"

        if filter.get('product_name'):
            query += " AND ph.`name` LIKE %(product_name)s"

        if type(filter.get('seller_attribute')) == int:
            query += " AND s.seller_subcategory_id = %(seller_attribute)s"

        if type(filter.get('seller_attribute')) == tuple:
            query += " AND s.seller_subcategory_id IN %(seller_attribute)s"

        if filter.get('order_by') == 1:
            query += " ORDER BY o.created_at DESC"

        else:
            query += " ORDER BY o.created_at ASC"

        query += " LIMIT %(offset)s, %(limit)s"

        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(query, filter)

            return cursor.fetchall()

    def get_product_prepare_count(self, connection, filter):
        query = f"""
            SELECT
                COUNT(*) AS count
            FROM orders AS o
                INNER JOIN order_products AS op
                    ON o.id = op.order_id
                INNER JOIN products AS p
                    ON op.product_id = p.id
                INNER JOIN order_histories AS oh
                    ON o.id = oh.order_id
                INNER JOIN order_product_histories AS oph
                    ON op.id = oph.order_product_id
                INNER JOIN product_histories AS ph
                    ON p.id = ph.product_id
                INNER JOIN seller_histories AS sh
                    ON p.seller_id = sh.seller_id
                INNER JOIN sellers AS s
                    ON sh.seller_id = s.id
                INNER JOIN shipments AS sm
                    ON op.id = sm.order_product_id
                INNER JOIN product_options AS po
                    ON op.product_option_id = po.id
                INNER JOIN sizes AS sz
                    ON po.size_id = sz.id
                INNER JOIN colors AS c
                    ON po.color_id = c.id
                INNER JOIN shipment_status AS ss
                    ON sm.shipment_status_id = ss.id
            WHERE
                sm.shipment_status_id = {SHIPMENT_STATUS_BEFORE_DELIVERY}
                AND o.created_at >= %(start_date)s
                AND o.created_at <= %(end_date)s
                """

        if filter.get('order_number'):
            query += " AND o.id LIKE %(order_number)s"

        if filter.get('order_detail_number'):
            query += " AND op.id LIKE %(order_detail_number)s"

        if filter.get('order_name'):
            query += " AND oh.`name` LIKE %(order_name)s"

        if filter.get('order_phone'):
            query += " AND oh.phone_number LIKE %(order_phone)s"

        if filter.get('seller_name'):
            query += " AND sh.korean_name LIKE %(seller_name)s"

        if filter.get('product_name'):
            query += " AND ph.`name` LIKE %(product_name)s"

        if type(filter.get('seller_attribute')) == int:
            query += " AND s.seller_subcategory_id = %(seller_attribute)s"

        if type(filter.get('seller_attribute')) == tuple:
            query += " AND s.seller_subcategory_id IN %(seller_attribute)s"

        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(query, filter)

            return cursor.fetchone()

    def patch_order_log_end(self, connection, order_product):
        query = f"""
            UPDATE  
                order_product_histories AS oph
            SET 
                oph.end_time = %(now)s
            WHERE 
                oph.order_status_id = {ORDER_STATUS_ORDER_COMPLETED}
                AND oph.order_product_id = %(order_product_id)s
                AND oph.end_time = %(end_date)s
            """

        with connection.cursor() as cursor:
            
            return cursor.execute(query, order_product)

    def patch_order_log_start(self, connection, order_product):
        query = f"""
            INSERT INTO 
                order_product_histories(
                    order_status_id,
                    order_product_id,
                    start_time,
                    end_time,
                    is_canceled,
                    price,
                    quantity
                )
            SELECT
                {SHIPPING},
                oph.order_product_id,
                %(now)s,
                %(end_date)s,
                oph.is_canceled,
                oph.price,
                oph.quantity
            FROM 
                order_product_histories AS oph
            WHERE
                oph.order_status_id = {ORDER_STATUS_ORDER_COMPLETED}
                AND oph.order_product_id = %(order_product_id)s
                AND oph.end_time = %(now)s
                """

        with connection.cursor() as cursor:
            
            return cursor.execute(query, order_product)

    def patch_shipments_info(self, connection, order_product):
        query = f"""
            UPDATE 
                shipments AS sm
            INNER JOIN order_products AS op
                ON sm.order_product_id = op.id
            INNER JOIN order_product_histories AS oph
                ON op.id = oph.order_product_id
            SET 
                sm.shipment_status_id = {SHIPPING},
                sm.start_time = %(now)s
            WHERE sm.order_product_id = %(order_product_id)s
                AND oph.order_status_id = {SHIPPING}
                AND oph.start_time = %(now)s
                AND oph.end_time = %(end_date)s
                """

        with connection.cursor() as cursor:

            return cursor.execute(query, order_product)