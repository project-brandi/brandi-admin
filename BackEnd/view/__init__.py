from view.user_view  import TestView
from view.order_view import ProductPrepareView 

def create_endpoints(app):
    app.add_url_rule('/order/product-prepare', view_func=ProductPrepareView.as_view('product_prepare'))
######################초기세팅########################
    app.add_url_rule('/test', view_func=TestView.as_view('test_view'))
######################초기세팅########################
