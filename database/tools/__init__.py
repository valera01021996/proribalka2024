from .product_tools import ProductTools
from .user_tools import UserTools
from .cart_tools import CartTools
from .order_tools import OrderTools
from .review_tools import ReviewTools
from .drive_tools import DriveTools
from .admin_tools import AdminTools
from .products_bu_tools import ProductToolsBU


class DBTools:
    def __init__(self):
        self.product_tools: ProductTools = ProductTools()
        self.user_tools: UserTools = UserTools()
        self.cart_tools: CartTools = CartTools()
        self.order_tools: OrderTools = OrderTools()
        self.review_tools: ReviewTools = ReviewTools()
        self.drive_tools: DriveTools = DriveTools()
        self.admin_tools: AdminTools = AdminTools()
        self.product_tools_bu: ProductToolsBU = ProductToolsBU()
