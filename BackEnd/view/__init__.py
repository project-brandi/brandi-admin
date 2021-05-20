from view.order_view import ProductPrepareView
from view.seller_view import AccountView
from view.product_view import ProductView


def create_endpoints(app):
    app.add_url_rule('/order/product-prepare', view_func=ProductPrepareView.as_view('product_prepare'))
    app.add_url_rule('/join/seller', view_func=AccountView.as_view('account_view'))
    app.add_url_rule("/products", view_func=ProductView.as_view("product_view"))
