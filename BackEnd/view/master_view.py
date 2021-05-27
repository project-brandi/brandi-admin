from flask                   import request, g
from flask.views             import MethodView

from service.master_service  import MasterService
from connection              import connect_db

from util.message            import UNAUTHORIZED
from util.exception          import UnauthorizedError
from util.const              import MASTER_ACCOUNT_TYPE
from util.decorator          import login_required

class MasterManageSellerView(MethodView):
    @login_required
    def get(self):
        data = g.account_info
            
        if data['account_type'] != MASTER_ACCOUNT_TYPE:
            raise UnauthorizedError(UNAUTHORIZED, 401)
        
        master_service = MasterService()
        connection = None
        try:
            filter = {
                "seller_id"          : request.args.get("seller_id", ""),
                "seller_nickname"    : request.args.get("seller_nickname", ""),
                "english_name"       : request.args.get("english_name", ""),
                "korean_name"        : request.args.get("korean_name", ""),
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
                result = master_service.get_seller_list(connection, filter)

            if request.path == "/manage/sellers/downloads":
                del filter["offset"]
                del filter["limit"]   
                result = master_service.to_xlsx(connection, filter)
            
            connection.commit()
            
            return result
        
        except Exception as e:
            connection.rollback()
            raise e 
            
        finally:
            if connection is not None:
                connection.close()