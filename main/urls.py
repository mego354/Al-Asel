from django.urls import path
from . import views_cbv as views

app_name = "main"
urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("", views.MakeOrderView.as_view(), name="make_order"),
    path("total_orders", views.total_orders, name="total_orders"),
    path("total_orders/month_sales", views.month_sales, name="month_sales"),
    path("users/", views.UsersView.as_view(), name="users"),
    path("users/all_orders", views.AllOrdersView.as_view(), name="all_orders"),
    path("users/all_coming_orders", views.AllComingOrdersView.as_view(), name="all_coming_orders"),
    path("users/<int:user_id>", views.UserDetailView.as_view(), name="user"),    
    path("order_info/<int:order_id>", views.OrderInfoView.as_view(), name="order_info"),
    path("order_info/<int:order_id>/add_items", views.AddItemsView.as_view(), name="add_items"),
    path("edit_order/<int:order_id>", views.EditOrderView.as_view(), name="edit_order"),
    path("change_rest", views.ChangeRestView.as_view(), name="change_rest"),
    path("put_rest", views.PutRestView.as_view(), name="put_rest"),
    path("delete_order/<int:order_id>", views.DeleteOrderView.as_view(), name="delete_order"),
    path("delete_order_item/<int:order_item_id>", views.DeleteOrderItemView.as_view(), name="delete_order_item"),
    path("change_rank/<int:order_id>", views.ChangeRankView.as_view(), name="change_rank"),
    path("order_error/<int:order_id>", views.OrderErrorView.as_view(), name="order_error"),
    path("create_item", views.CreateItemView.as_view(), name="create_item"),
    path("coming_order", views.coming_order, name="coming_order"),
    path("coming_order/<int:order_id>", views.coming_order_info, name="coming_order_info"),
    path("coming_order/<int:order_id>/add_items", views.add_coming_items, name="add_coming_items"),
    path("coming_put_rest", views.coming_put_rest, name="coming_put_rest"),
    path("coming_change_rest", views.coming_change_rest, name="coming_change_rest"),

    path("edit_coming_item/<int:item_id>", views.edit_coming_item, name="edit_coming_item"),
    path("delete_coming_item/<int:item_id>", views.delete_coming_item, name="delete_coming_item"),
    path("delete_coming_order/<int:order_id>", views.delete_coming_order, name="delete_coming_order"),
    path("done_coming_order/<int:order_id>", views.done_coming_order, name="done_coming_order"),
    path("store_info/<int:store_id>", views.store_coming_info, name="store_coming_info"),
    path("supplier_info/<int:supplier_id>", views.supplier_coming_info, name="supplier_coming_info"),
    path("create_category", views.CreateCategoryView.as_view(), name="create_category"),
    path("create_customer", views.CreateCustomerView.as_view(), name="create_customer"),
    path("all_rest_orders", views.all_rest_orders, name="all_rest_orders"),
    path("all_rest_coming_orders", views.all_rest_coming_orders, name="all_rest_coming_orders"),

    # Management URLs
    path("manage/categories", views.CategoryManagementView.as_view(), name="category_management"),
    path("manage/items", views.ItemManagementView.as_view(), name="item_management"),
    path("manage/categories/<int:category_id>/delete", views.DeleteCategoryView.as_view(), name="delete_category"),
    path("manage/items/<int:item_id>/delete", views.DeleteItemView.as_view(), name="delete_item"),
    path("manage/categories/<int:category_id>/update", views.UpdateCategoryView.as_view(), name="update_category"),
    path("manage/items/<int:item_id>/update", views.UpdateItemView.as_view(), name="update_item_management"),
    # Help page
    path("help", views.HelpView.as_view(), name="help"),
    ###################### api ######################         
    path("users_search/<str:text>", views.UsersSearchView.as_view(), name="users_search"),
]
 