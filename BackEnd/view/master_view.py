from flask                             import request, jsonify, g
from flask.views                       import MethodView
from flask_request_validator.validator import JSON, Param, validate_params

from service.master_service  import MasterService
from connection              import connect_db

from util.message            import UNAUTHORIZED, STATUS_UPDATE_SUCCESS
from util.exception          import UnauthorizedError
from util.const              import MASTER_ACCOUNT_TYPE
from util.decorator          import login_required

class MasterManageSellerView(MethodView):
    @login_required
    def get(self):
        auth = g.account_info
            
        if auth['account_type'] != MASTER_ACCOUNT_TYPE:
            raise UnauthorizedError(UNAUTHORIZED, 401)
        
        master_service = MasterService()
        connection = None
        try:
            filter = {
                "seller_id"          : request.args.get("seller_id", ""),
                "seller_nickname"    : request.args.get("seller_nickname", ""),
                "english_name"       : request.args.get("english_name", ""),
                "korean_name"        : request.args.get("korean_name", ""),
                "seller_type"        : request.args.get("seller_type", ""),
                "clerk_name"         : request.args.get("clerk_name", ""),
                "clerk_phone_number" : request.args.get("clerk_phone_number", ""),
                "clerk_email"        : request.args.get("clerk_email", ""),
                "start_date"         : request.args.get("start_date", ""),
                "end_date"           : request.args.get("end_date", ""),
                "action_status"      : request.args.get("action_status", ""),
                "offset"             : int(request.args.get("offset", 0)),
                "limit"              : int(request.args.get("limit", 10)),
            }
            
            connection = connect_db()

            if request.path == "/manage/sellers":
                result, count = master_service.get_seller_list(connection, filter)
                return jsonify({"data" : result, "count" : count}), 200

            if request.path == "/manage/sellers/downloads":
                del filter["offset"]
                del filter["limit"]   
                result = master_service.to_xlsx(connection, filter)
                return result
            
        except Exception as e:
            connection.rollback()
            raise e 
            
        finally:
            if connection is not None:
                connection.close()
    
    @login_required
    @validate_params(
        Param("seller_id", JSON, int, required=True),
        Param("master_action_id", JSON, int, required=True)
    )
    def patch(*args):
        auth = g.account_info
            
        if auth['account_type'] != MASTER_ACCOUNT_TYPE:
            raise UnauthorizedError(UNAUTHORIZED, 401)
        
        master_service = MasterService()
        connection = None
        try:
            data = request.json
            data["account_id"] = auth["account_id"]

            connection = connect_db()
            result = master_service.change_seller_status(connection, data)
            connection.commit()

            return jsonify({"message" : STATUS_UPDATE_SUCCESS, "data" : result}), 201

        except Exception as e:
            connection.rollback()
            raise e
        
        finally:
            if connection is not None:
                connection.close()
