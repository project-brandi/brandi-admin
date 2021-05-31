import pymysql

class OrderDetailInfoDao:
    def get_order_detail_info(self, connection, data):
        query = """
            SELECT 
                o.id as order_id,
                o.created_at as order_created_at,
                oh.total_price, 
                op.id as order_product_id, 
                os.order_status, 
                o.paid_at, 
                oph.order_status_id, 
                uh.phone_number as order_phone, 
                p.id, 
                ph.`name`, 
                oph.price, 
                oph.discount_rate, 
                sh.korean_name, 
                sz.size, 
                c.color, 
                oph.quantity, 
                u.id, 
                oh.`name` as order_name, 
                adh.`name`as receive_name, 
                adh.phone_number as receive_phone, 
                adh.address, 
                smm.content, 
                sm.message
            FROM order_products as op
            INNER JOIN orders AS o 
                ON op.order_id = o.id
            INNER JOIN order_histories AS oh 
            ON o.id = oh.order_id
            INNER JOIN order_product_histories AS oph 
                ON op.id = oph.order_product_id
            INNER JOIN order_status AS os 
                ON oph.order_status_id = os.id 
            INNER JOIN users AS u 
                ON o.user_id = u.id 
            INNER JOIN user_histories as uh 
                ON u.id = uh.user_id 
            INNER JOIN product_options as po 
                ON op.product_option_id = po.id 
            INNER JOIN products as p 
                ON po.product_id = p.id 
            INNER JOIN product_histories as ph 
                ON p.id = ph.product_id 
            INNER JOIN sellers as s 
                ON p.seller_id = s.id 
            INNER JOIN seller_histories as sh 
                ON s.id = sh.seller_id 
            INNER JOIN sizes as sz 
                ON po.size_id = sz.id 
            INNER JOIN colors as c 
                ON po.color_id = c.id 
            INNER JOIN shipments as sm 
                ON op.id = sm.order_product_id 
            INNER JOIN addresses as ad 
                ON sm.address_id = ad.id 
            INNER JOIN address_histories as adh 
                ON ad.id = adh.address_id 
            INNER JOIN shipment_memo as smm 
                ON sm.shipment_memo_id = smm.id 
            WHERE op.id = %(order_product_id)s
                AND oph.end_time = %(end_date)s
            """
        
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(query, data)
        
            return cursor.fetchone()

    def get_order_log(self, connection, data):
        query = """
            SELECT 
                oph.start_time, 
                os.order_status 
            FROM order_product_histories as oph 
            INNER JOIN order_status AS os 
                ON oph.order_status_id = os.id 
            WHERE oph.order_product_id = %(order_product_id)s
            """
        
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(query, data)

            return cursor.fetchall()