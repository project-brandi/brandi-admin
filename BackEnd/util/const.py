"""Constants used by Dao"""

# 이력 종료 시점
END_DATE = '9999-12-31 23:59:59'

# Seller Action Status
OPEN_STORE = 1
STAND_BY = 2

# 유저 타입
MASTER = 1
SELLER = 2
USER = 3

# shipments_status 배송준비중
SHIPMENT_STATUS_BEFORE_DELIVERY = 1

# order_status 주문완료
ORDER_STATUS_ORDER_COMPLETED = 1

# shipments_status, order_status 배송 중
SHIPPING = 2

# shipments_status, order_status 배송 완료
DELIVERY_COMPLETED = 3
