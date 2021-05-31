from flask                   import request, jsonify
from flask.views             import MethodView
from flask_request_validator import validate_params, Param, GET

from service        import OrderDetailInfoService
from util.decorator import login_required
from connection     import connect_db

class OrderDetailInfoView(MethodView):
    @login_required
    @validate_params(
        Param("order_product_id", GET, int, required=True)
    )
    def get(self, *args):
        order_detail_info = OrderDetailInfoService()

        connection = None
        try:
            connection = connect_db()
            
            data = dict(request.args)
            
            result = order_detail_info.get_order_detail_info(connection, data)
            
            return jsonify(result), 200

        except Exception as e:
            if connection is not None:
                connection.rollback()
            raise e
        
        finally:
            if connection is not None:
                connection.close()
