from view.order_view   import ProductPrepareView
from view.product_view import ProductView
from view.order_view   import ProductPrepareView 
from view.seller_view  import SellerAccountView, MasterAccountView, LoginView

def create_endpoints(app):
    app.add_url_rule('/order/product-prepare', view_func=ProductPrepareView.as_view('product_prepare'))
    app.add_url_rule('/join/sellers', view_func=SellerAccountView.as_view('seller_account_view'))
    app.add_url_rule('/join/masters', view_func=MasterAccountView.as_view('master_account_view'))
    app.add_url_rule("/products", view_func=ProductView.as_view("product_view"))
    app.add_url_rule('/login', view_func=LoginView.as_view('login_view'))