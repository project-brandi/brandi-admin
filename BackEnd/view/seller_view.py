from flask                   import request, jsonify
from flask.views             import MethodView
from flask_request_validator import JSON, Param, validate_params
                                    
from service.seller_service  import AccountService
from connection              import connect_db
from util.validation         import nickname_rule, password_rule, phone_number_rule 
from util.message            import ACCOUNT_CREATED

class AccountView(MethodView):
    @validate_params(
        Param('nickname', JSON, str, required=True, rules=[nickname_rule]),
        Param('account_type_id', JSON, int, required=True),
        Param('password', JSON, str, required=True, rules=[password_rule]),
        Param('seller_subcategory_id', JSON, int, required=False),
        Param('seller_phone_number', JSON, str, required=False, rules=[phone_number_rule]),
        Param('korean_name', JSON, str, required=False),
        Param('english_name', JSON, str, required=False),
        Param('cs_phone_number', JSON, str, required=False, rules=[phone_number_rule]),
        Param('cs_nickname', JSON, str, required=False)
    )
    def post(*args):
        account_service = AccountService()

        connection = None
        try:
            data = request.json
            
            connection = connect_db()
            result     = account_service.create_account(data, connection)
            connection.commit()
            
            return jsonify({"message" : ACCOUNT_CREATED, "data" : result})
        
        except Exception as e:
            connection.rollback()
            raise e 
            
        finally:
            if connection is not None:
                connection.close()