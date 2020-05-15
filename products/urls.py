from django.urls import path
from . import views

urlpatterns = [
    path('payment/stripe/',views.PaymentView , name='payment'),
    path('cart/', views.CartView, name='cart'),
    path('addToCart/<str:id>/',views.AddToCartView , name='AddToCart'),
    path('remove/<str:id>/',views.RemoveFromCartView , name='remove'),
    path('checkout/',views.CheckoutView , name='checkout'),
    path('addcoupon/',views.AddCouponCodeView , name='addcoupon'),
    path('',views.ProductView.as_view() , name='home'),
    path('refund/',views.RefunView.as_view() , name='refund'),
    path('<str:name>/',views.ProductlistOnCategoryView , name='productsoncategory'),
    path('DeleteItem/<str:id>/',views.DeleteItem , name='DeleteItem'),
    path('detiels/<str:pk>/',views.DetiailsView , name='det'),
    path('accounts/profile/<str:pk>/', views.ProfileView, name='profile')
]




