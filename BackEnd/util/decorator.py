import jwt

from functools        import wraps
from flask            import request, g

from model.seller_dao import AccountDao
from util.exception   import InvalidAccessError, LoginRequiredError
from util.message     import UNAUTHORIZED_TOKEN, LOGIN_REQUIRED
from config           import SECRET_KEY, ALGORITHM
from connection       import connect_db

def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        access_token = request.headers.get('Authorization')
        if access_token is not None:
            try:
                payload = jwt.decode(access_token, SECRET_KEY['secret'], ALGORITHM)

            except jwt.InvalidTokenError:
                payload = None
            
            if payload is None:
                raise InvalidAccessError(UNAUTHORIZED_TOKEN, 401)

            data         = {'account_id' : payload['Id']}
            account_dao  = AccountDao()
            connection   = connect_db()
            
            if payload['account_type'] == 'seller':
                is_deleted = account_dao.is_deleted_seller(data, connection)['is_deleted']
                if is_deleted:
                    raise InvalidAccessError(UNAUTHORIZED_TOKEN, 401)

            if payload['account_type'] == 'master':
                is_deleted = account_dao.is_deleted_master(data, connection)['is_deleted']
                if is_deleted:
                    raise InvalidAccessError(UNAUTHORIZED_TOKEN, 401)

            g.account_info = {'account_id' : payload['Id'], 'account_type' : payload['account_type']}
        else:
            raise LoginRequiredError(LOGIN_REQUIRED, 401)   
        
        return func(*args, **kwargs)
    return wrapper