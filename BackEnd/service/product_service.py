import re

from model.product_dao import ProductDao


class ProductService:

    def get_product_list(self, connection, filters):
        """어드민 상품 관리 리스트

        Author:
            SeoJin Lee

        Returns:
            "count": 상품 리스트 총 개수
            "products": [
                {
                    "created_at": 상품 등록 시간,
                    "discount_start_time": 상품 할인 시작 시간,
                    "discount_end_time": 상품 할인 끝 시간,
                    "discount_rate": 상품 할인율,
                    "image_url": 상품 대표 이미지 주소,
                    "is_displayed": 진열 여부,
                    "is_sold": 판매 여부,
                    "name": 상품 이름,
                    "price": 가격,
                    "product_code": 상품 코드,
                    "product_number": 상품 번호,
                    "seller_category": 셀러 속성
                }
            ]
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

        reg = re.compile(r'[a-zA-Z]')

        # filters에 seller_name이 있으면서 영어 대소문자와 숫자로 이루어졌을 때
        if filters.get("seller_name") and reg.match(filters.get("seller_name")):
            filters["seller_name_en"] = filters["seller_name"] + '%'

        # filters에 seller_name이 있으면서 영어 대소문자와 숫자로 이루어지지 않았을 때
        if filters.get("seller_name") and not reg.match(filters.get("seller_name")):
            filters["seller_name_kr"] = filters["seller_name"] + '%'

        # 셀러 속성 리스트는 ,로 잘라서 튜플로 변환
        if "seller_category" in filters:
            filters["seller_category"] = tuple(filters["seller_category"].split(","))

        filters["offset"] = int(filters.get("offset", 0))
        filters["limit"] = int(filters.get("limit", 10))

        if filters.get("offset") < 0:
            filters["offset"] = 0

        if filters.get("limit") < 1:
            filters["limit"] = 1

        product_dao = ProductDao()
        products = product_dao.get_product_list(connection, filters)
        count = product_dao.get_product_list(connection, filters, is_count=True)

        return {"products": products, "count": count[0]["count"]}
