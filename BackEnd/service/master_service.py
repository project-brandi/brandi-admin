from flask.json       import jsonify

from model.master_dao     import MasterDao
from service.util_service import ExcelDownloadService

class MasterService:
    def get_seller_list(self, connection, filter):
        master_dao = MasterDao()

        try:
            result = master_dao.get_seller_list(connection, filter)
            count  = master_dao.get_seller_list_count(connection, filter)

            return jsonify({"data" : result, "count" : count["count"]}), 200

        except Exception as e:
            raise e

    def to_xlsx(self, connection, filter):
        get_data_dao = MasterDao()
        to_xlsx_service = ExcelDownloadService()

        try:
            data = get_data_dao.get_seller_list(connection, filter)

            titles = [
                "번호",
                "셀러아이디",
                "영문이름",
                "한글이름",
                "담당자이름",
                "셀러상태",
                "담당자연락처",
                "담당자이메일",
                "셀러속성",
                "상품개수",
                "등록일시"
            ]

            for item in data:
                item["created_at"] = str(item["created_at"])

            result = to_xlsx_service.excel_download(titles, data)

            return result

        except Exception as e:
            raise e
        