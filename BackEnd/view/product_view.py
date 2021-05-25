from flask import jsonify, request, g
from flask.views import MethodView
from flask_request_validator import GET, Param, validate_params, Datetime, CompositeRule, Max, Min

from service.product_service import ProductService

from connection import connect_db


class ProductView(MethodView):

    # 로그인 여부 데코레이터
    @validate_params(
        Param("start_date", GET, str, required=False, rules=[Datetime('%Y-%m-%d')]),
        Param("end_date", GET, str, required=False, rules=[Datetime('%Y-%m-%d')]),
        Param("seller_name", GET, str, required=False),
        Param("product_name", GET, str, required=False),
        Param("product_number", GET, int, required=False),
        Param("is_sold", GET, bool, required=False),
        Param("is_displayed", GET, bool, required=False),
        Param("is_sale", GET, bool, required=False),
        Param("seller_category", GET, list, required=False),
        Param("offset", GET, int, required=False),
        Param("limit", GET, int, required=False, rules=CompositeRule(Min(1), Max(100)))
    )
    def get(*args):
        """어드민 상품 관리 리스트

        Author:
            이서진

        Returns:
            200: {
                "data": {
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
                }
            }
            400: validate param 오류
        """

        filters = dict(request.args)

        filters["account_type"] = "master"
        filters["account_id"] = "1"

        product_service = ProductService()
        connection = None

        try:
            connection = connect_db()
            result = product_service.get_product_list(connection, filters)
            return jsonify({"data": result})

        except Exception as e:
            raise e

        finally:
            if connection is not None:
                connection.close()

    def patch(*args):
        data = request.json

        product_service = ProductService()
        connection = None

        try:
            connection = connect_db()
            result = product_service.update_product_list(connection, data)
            return jsonify({"data": result})

        except Exception as e:
            raise e

        finally:
            if connection is not None:
                connection.close()
