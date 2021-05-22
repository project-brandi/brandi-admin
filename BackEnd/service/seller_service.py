import bcrypt

from model.seller_dao import AccountDao
from util.exception   import AlreadyExistError
from util.message     import ALREADY_EXISTS
from util.const       import STAND_BY

#################################초기세팅#############################
class AccountService:
    """
    어드민 회원가입 중 입력받은 닉네임이 DB에 없으면
    join을 호출하여 가입을 허용하고 그렇지 않은 경우
    ALREADY_EXISTS 메세지를 리턴한다.

    가입이 허용되는 경우 account_type을 확인하여 
    seller인지 master인지 구분하고 각각의 마스터 테이블과
    이력 테이블에 정보를 삽입한다. 
    """
    def create_account(self, data, connection):    
        
        account_dao = AccountDao()
        is_existed  = account_dao.is_existed_account(data, connection)
        
        if is_existed:
            raise AlreadyExistError(ALREADY_EXISTS, 400)

        account_id         = account_dao.join(data,connection)
    
        data['Id']         = account_id
        data['account_id'] = account_id
        account_type       = account_dao.get_account_type(data, connection)['account_type']
            
        hashed_password  = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        data['password'] = hashed_password

        if account_type == 'seller':
            account_dao.seller_join_info(data, connection)
            data['seller_id']        = account_id
            data['action_status_id'] = STAND_BY
            return account_dao.seller_join_history(data, connection)
        
        if account_type == 'master':
            account_dao.master_join_info(data, connection) 
            data['master_id'] = account_id
            return account_dao.master_join_history(data, connection)

        

                


            