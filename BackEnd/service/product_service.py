import re

from model.product_dao import ProductDao


class ProductService:

    def get_product_list(self, connection, filters):
        """어드민 상품 관리 리스트

        Author:
            SeoJin Lee

        Returns:
        """

        # 조회 기간 필터에서 시작 날짜가 끝 날짜보다 뒤일 때 시작과 끝을 같게 해줌
        if "start_date" and "end_date" in filters:
            if filters.get("start_date") > filters.get("end_date"):
                filters["start_date"] = filters["end_date"]

        if "start_date" in filters:
            filters["start_date"] = filters["start_date"] + ' 00:00:00'

        if "end_date" in filters:
            filters["end_date"] = filters["end_date"] + ' 23:59:59'

        if "product_name" in filters:
            filters["product_name"] = filters["product_name"] + '%'

        if filters.get("is_sold") == "true":
            filters["is_sold"] = True

        if filters.get("is_sold") == "false":
            filters["is_sold"] = False

        if filters.get("is_displayed") == "true":
            filters["is_displayed"] = True

        if filters.get("is_displayed") == "false":
            filters["is_displayed"] = False

        if filters.get("is_sale") == "true":
            filters["is_sale"] = True

        if filters.get("is_sale") == "false":
            filters["is_sale"] = False

        reg = re.compile(r'[a-zA-Z0-9]')

        # filters에 seller_name이 있으면서 영어 대소문자와 숫자로 이루어졌을 때
        if filters.get("seller_name") and reg.match(filters.get("seller_name")):
            filters["seller_name_en"] = filters["seller_name"] + '%'

        # filters에 seller_name이 있으면서 영어 대소문자와 숫자로 이루어지지 않았을 때
        if filters.get("seller_name") and not reg.match(filters.get("seller_name")):
            filters["seller_name_kr"] = filters["seller_name"] + '%'

        # 셀러 속성 리스트는 ,로 잘라서 튜플로 변환
        if "seller_category" in filters:
            filters["seller_category"] = tuple(filters["seller_category"].split(","))

        filters["offset"] = filters.get("offset", 0)
        filters["limit"] = filters.get("limit", 10)

        product_dao = ProductDao()
        products = product_dao.get_product_list(connection, filters)
        count = product_dao.get_product_list(connection, filters, is_count=True)

        return {"products": products, "count": count[0]["count"]}

