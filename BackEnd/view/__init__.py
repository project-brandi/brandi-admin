from view.order_view   import ProductPrepareView, OrderDetailInfoView
from view.product_view import ProductView, ProductSellerView
from view.account_view  import SellerAccountView, MasterAccountView, LoginView
from view.master_view  import MasterManageSellerView

def create_endpoints(app):
    app.add_url_rule('/order/product-prepare', view_func=ProductPrepareView.as_view('product_prepare'))
    app.add_url_rule("/join/sellers", view_func=SellerAccountView.as_view("seller_account_view"))
    app.add_url_rule("/join/masters", view_func=MasterAccountView.as_view("master_account_view"))
    app.add_url_rule("/login", view_func=LoginView.as_view("login_view"))
    app.add_url_rule("/manage/sellers", view_func=MasterManageSellerView.as_view("master_manage_seller_view"))
    app.add_url_rule("/manage/sellers/downloads", view_func=MasterManageSellerView.as_view("master_manage_seller_download_view"))
    app.add_url_rule('/order/product-prepare/download', view_func=ProductPrepareView.as_view('excel_download'))
    app.add_url_rule("/order/order_detail_info", view_func=OrderDetailInfoView.as_view("order_detail_info"))

    app.add_url_rule("/products", view_func=ProductView.as_view("product_view"))
    app.add_url_rule("/products/seller", view_func=ProductSellerView.as_view("product_seller_view"))
