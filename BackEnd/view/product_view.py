from flask import jsonify, request, g
from flask.views import MethodView
from flask_request_validator import GET, Param, validate_params, Datetime, CompositeRule, Max, Min

from service import ProductService

from util.decorator import login_required
from util.const import MASTER, SELLER
from util.message import UNAUTHORIZED, NOT_EXIST_PRODUCT_ID, INVALID_PRODUCT_ID
from util.exception import UnauthorizedError, InvalidParamError

from connection import connect_db


class ProductView(MethodView):

    @login_required
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
        filters["account_id"] = g.account_info.get("account_id")

        if g.account_info.get("account_type") not in [MASTER, SELLER]:
            raise UnauthorizedError(UNAUTHORIZED, 401)

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

    # 로그인 데코레이터
    def patch(*args):
        data = request.json

        for row in data:
            # product_id가 없을 때
            if row.get("product_id") is None:
                raise InvalidParamError(NOT_EXIST_PRODUCT_ID, 400)

            # product_id가 숫자가 아닐 때
            if type(row.get("product_id")) is not int:
                raise InvalidParamError(INVALID_PRODUCT_ID, 400)

        product_service = ProductService()
        connection = None

        try:
            connection = connect_db()
            result = product_service.update_product_list(connection, data)
            return jsonify({"data": result})

        except Exception as e:
            connection.rollback()
            raise e

        finally:
            if connection is not None:
                connection.close()


class ProductSellerView(MethodView):

    @validate_params(
        Param("search_word", GET, str, required=True),
        Param("limit", GET, int, required=True, rules=CompositeRule(Min(1), Max(100)))
    )
    def get(*args):
        # TODO
        # 1. 셀러 속성 갖고 오기
        # 2. 입점 준비 중인 셀러는 아예 목록에 안뜨게

        filters = dict(request.args)

        product_service = ProductService()
        connection = None

        try:
            connection = connect_db()
            result = product_service.get_seller_name_search_list(connection, filters)
            return jsonify({"data": result})

        except Exception as e:
            raise e

        finally:
            if connection is not None:
                connection.close()
