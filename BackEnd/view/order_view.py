from datetime import datetime, date, timedelta
from ast      import literal_eval

from flask                             import jsonify, request, g
from flask.views                       import MethodView

from connection     import connect_db
from service        import ProductPrepareService
from util.exception import InvalidRequest, OffsetOutOfRangeError, LimitOutOfRangeError, ParamRequiredError
from util.message   import *
from util.decorator import login_required
from util.const     import SELLER_ACCOUNT_TYPE

class ProductPrepareView(MethodView):
    # validate_parms 변경 예정
    @login_required
    def get(self):
        product_prepare_service = ProductPrepareService()

        connection = None

        try:
            filter = {
                "order_id"         : request.args.get("order_id", ""),
                "order_product_id" : request.args.get("order_product_id", ""),
                "order_name"       : request.args.get("order_name", ""),
                "order_phone"      : request.args.get("order_phone", ""),
                "start_date"       : request.args.get("start_date", ""),
                "end_date"         : request.args.get("end_date", ""),
                "seller_name"      : request.args.get("seller_name", ""),
                "product_name"     : request.args.get("product_name", ""),
                "seller_attribute" : request.args.get("seller_attribute", ""),
                "order_by"         : int(request.args.get("order_by", 1)),
                "offset"           : int(request.args.get("offset", 0)),
                "limit"            : int(request.args.get("limit", 50)),
            }

            if filter["order_id"] == "" and\
                filter["order_product_id"] == "" and\
                filter["order_name"] == "" and \
                filter["order_phone"] == "" and\
                filter["start_date"] == "" and\
                filter["end_date"] == "":
                raise ParamRequiredError(PARAM_REQUIRED, 400)

            if filter["offset"] < 0:
                raise OffsetOutOfRangeError(OFFSET_OUT_OF_RANGE, 400)
            
            if filter["limit"] < 1:
                raise LimitOutOfRangeError(LIMIT_OUT_OF_RANGE, 400)

            if filter["seller_attribute"] != "":
                filter["seller_attribute"] = literal_eval(filter["seller_attribute"])
            
            if filter["end_date"] != "":
                filter["end_date"] = datetime.strptime(filter["end_date"], '%Y-%m-%d') + timedelta(days=1)            
            
            if g.account_info["account_type"] == SELLER_ACCOUNT_TYPE:
                filter["account_id"] = g.account_info["account_id"]

            connection = connect_db()

            if request.path == '/order/product-prepare':
                result =  product_prepare_service.get_product_prepare(connection, filter)

            if request.path == '/order/product-prepare/download':
                if filter["order_product_id"]:
                    filter["order_product_id"] = literal_eval(filter["order_product_id"])
                
                del filter["offset"]
                del filter["limit"]
                
                result = product_prepare_service.excel_download(connection, filter)

            return result

        except Exception as e:
            if connection is not None:
                connection.rollback()
            raise e

        finally:
            if connection is not None:
                connection.close() 

    @login_required
    def patch(self):
        product_prepare_service = ProductPrepareService()
        
        connection = None

        try:
            data = request.json

            if "order_products" not in data:
                raise InvalidRequest(ORDER_PRODUCTS_NEEDED, 400)

            order_products = data["order_products"]

            for order_product in order_products:
                if "order_product_id" not in order_product:
                    raise InvalidRequest(ORDER_PRODUCT_ID_NEEDED, 400)
                if g.account_info["account_type"] == SELLER_ACCOUNT_TYPE:
                    order_product["account_id"] = g.account_info["account_id"]

            connection = connect_db()

            result = product_prepare_service.patch_product_prepare(connection, order_products)
            
            return jsonify(result), 200

        except Exception as e:
                raise e

        finally:
            if connection is not None:
                connection.close()