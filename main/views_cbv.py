from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse, HttpRequest
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.contrib.auth import login, logout, authenticate
import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView, View
from django.views.generic.edit import FormView
from django.contrib import messages
from django.db.models import Q, Sum, Count
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from .models import Customer, Order, Item, OrderItem, Category, Store_Order, Store_OrderItem
from .forms import CategoryForm, CustomerForm, ItemForm
from decimal import Decimal, InvalidOperation
import datetime


class LoginView(TemplateView):
    template_name = "main/login.html"
    
    def get(self, request, *args, **kwargs):
        full_url = request.get_full_path()
        index_url = full_url.find('=')
        if index_url > 0:
            url = full_url[index_url + 1:]
        else:
            url = 0
        return render(request, self.template_name, {"url": url})

    def post(self, request, *args, **kwargs):
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            url = request.POST["url"]
            if url and url != "0":
                return HttpResponseRedirect(url)
            return HttpResponseRedirect("/")
        else:
            return render(request, self.template_name, {
                "err_message": "هناك خطأ في الأسم او الرقم السري"
            })


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return render(request, "main/login.html", {
            "success_message": "تم تسجيل خروجك بنجاح "
        })


class MakeOrderView(LoginRequiredMixin, TemplateView):
    template_name = "main/make_order.html"
    login_url = "/login/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        items_object = {}
        categories = Category.objects.all()
        for category in categories:
            items = Item.objects.filter(category=category).order_by('id')
            items_object[f"{category.name}"] = items

        context.update({
            "items_object": items_object,
            "customers": Customer.objects.all(),
        })
        return context

    def post(self, request, *args, **kwargs):
        items_object = {}
        categories = Category.objects.all()
        for category in categories:
            items = Item.objects.filter(category=category).order_by('id')
            items_object[f"{category.name}"] = items

        customer_id = request.POST["customer"]
        customer = Customer.objects.get(id=customer_id)
        market_or_gomla = request.POST["market_or_gomla"]
        
        check_order = False
        if market_or_gomla == "market":
            order = Order.objects.create(customer=customer)
        else:
            order = Order.objects.create(customer=customer, is_gomla=True)
        
        for category in items_object.values():
            for item in category:
                try:
                    quantity = int(request.POST[f"quantity_{item.id}"])
                except ValueError:
                    quantity = 0
                if quantity > 0:
                    OrderItem.objects.create(order=order, item=item, quantity=quantity)
                    check_order = True

        if check_order == False:
            order.delete()
            return HttpResponseRedirect("/")

        return HttpResponseRedirect(f"/order_info/{order.id}")


class AddItemsView(LoginRequiredMixin, TemplateView):
    template_name = "main/add_items.html"
    login_url = "/login/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order_id = self.kwargs.get('order_id')
        order = get_order(order_id)
        
        if not order:
            return context

        items_object = {}
        categories = Category.objects.all()
        un_wanted_items = OrderItem.objects.filter(order=order).values_list('item', flat=True)

        for category in categories:
            items = Item.objects.exclude(id__in=un_wanted_items)
            items_object[f"{category.name}"] = items.filter(category=category)

        context.update({
            "items_object": items_object,
            "order": order
        })
        return context

    def post(self, request, *args, **kwargs):
        order_id = self.kwargs.get('order_id')
        order = get_order(order_id)
        
        if not order:
            return HttpResponseRedirect(f"/order_error/{order_id}")

        items_object = {}
        categories = Category.objects.all()
        un_wanted_items = OrderItem.objects.filter(order=order).values_list('item', flat=True)

        for category in categories:
            items = Item.objects.exclude(id__in=un_wanted_items)
            items_object[f"{category.name}"] = items.filter(category=category)

        for category in items_object.values():
            for item in category:
                try:
                    quantity = int(request.POST.get(f"quantity_{item.id}"))
                except ValueError:
                    quantity = 0

                if quantity > 0:
                    OrderItem.objects.create(order=order, item=item, quantity=quantity)

        return HttpResponseRedirect(f"/order_info/{order_id}")


class OrderInfoView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = "main/order_info.html"
    context_object_name = "order"
    pk_url_kwarg = "order_id"
    login_url = "/login/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order = self.get_object()
        context['order_items'] = OrderItem.objects.filter(order=order)
        return context

    def get_object(self, queryset=None):
        order_id = self.kwargs.get('order_id')
        order = get_order(order_id)
        if not order:
            return HttpResponseRedirect(f"/order_error/{order_id}")
        return order


class UsersView(LoginRequiredMixin, TemplateView):
    template_name = "main/users_display.html"
    login_url = "/login/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "customers": Customer.objects.all().order_by("-is_shop", "id"),
            "orders": Order.objects.filter(is_used=True).order_by("-id"),
        })
        return context

    def post(self, request, *args, **kwargs):
        customer_id = request.POST["customer_id"]
        order_id = request.POST["order_id"]

        if customer_id and not order_id:
            if customer_id.isnumeric():
                return HttpResponseRedirect(f"{customer_id}")
            else:
                customer_name_for_id = Customer.objects.filter(name__contains=customer_id).first()
                if customer_name_for_id:
                    return HttpResponseRedirect(f"{customer_name_for_id.id}")
        elif order_id.isnumeric() and not customer_id:
            return HttpResponseRedirect(f"/order_info/{order_id}")

        return HttpResponseRedirect("/users/")


class AllOrdersView(LoginRequiredMixin, TemplateView):
    template_name = "main/all_orders.html"
    login_url = "/login/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        orders = Order.objects.filter(is_used=True).order_by("-created_at")
        dates = orders.values_list("created_at", flat=True)
        years = {}
        
        for date in dates:
            date = change_zone(date)
            if not date.year in years.keys():
                years[f"{date.year}"] = orders.filter(created_at__range=(datetime.date(date.year, 1, 1), datetime.date(date.year + 1, 1, 1)))

        context['years'] = years
        return context


class AllComingOrdersView(LoginRequiredMixin, TemplateView):
    template_name = "main/all_coming_orders.html"
    login_url = "/login/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        orders = Store_Order.objects.all().order_by("-created_at")
        dates = orders.values_list("created_at", flat=True)
        years = {}
        
        for date in dates:
            date = change_zone(date)
            if not date.year in years.keys():
                years[f"{date.year}"] = orders.filter(created_at__range=(datetime.date(date.year, 1, 1), datetime.date(date.year + 1, 1, 1)))

        context['years'] = years
        return context


class UserDetailView(LoginRequiredMixin, DetailView):
    model = Customer
    template_name = "main/user_display.html"
    context_object_name = "customer"
    pk_url_kwarg = "user_id"
    login_url = "/login/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        customer = self.get_object()
        
        if not customer:
            return context

        arranged_orders = {}
        orders = customer.orders.all().order_by('-created_at')
        
        for order in orders:
            order_time = change_zone(order.created_at)
            y = order_time.strftime("%y")
            m = order_time.strftime("%m")
            d = order_time.strftime("%d")
            
            if str(y) not in arranged_orders.keys():
                arranged_orders[f"{y}"] = {}
            if str(m) not in arranged_orders[f"{y}"].keys():
                arranged_orders[f"{y}"][f"{m}"] = {}
            if str(d) not in arranged_orders[f"{y}"][f"{m}"].keys():
                arranged_orders[f"{y}"][f"{m}"][f"{d}"] = []
            arranged_orders[f"{y}"][f"{m}"][f"{d}"].append(order)

        total_orders_info = get_total_orders_info(customer, "all")
        rest_info = get_rest_info(customer)
        total_money = get_total_orders_info(customer, 0)

        context.update({
            "orders": orders,
            "arranged_orders": arranged_orders,
            "total_orders_info": total_orders_info,
        })

        if not total_orders_info:
            return context

        if total_orders_info and rest_info and total_money:
            percent = (total_money - rest_info["rest_money"]) / total_money * 100
        elif total_orders_info and not rest_info:
            percent = 100

        context.update({
            "rest_info": rest_info,
            "percent": int(percent),
        })

        return context

    def post(self, request, *args, **kwargs):
        order_id = request.POST["order_id"]
        order = get_order(order_id)
        if not order:
            return HttpResponseRedirect(f"/order_error/{order_id}")
        return HttpResponseRedirect(f"/edit_order/{order.id}")


class EditOrderView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = "main/order_info.html"
    context_object_name = "order"
    pk_url_kwarg = "order_id"
    login_url = "/login/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order = self.get_object()
        context.update({
            "order_items": OrderItem.objects.filter(order=order),
            "is_gomla": order.is_gomla,
            "message_edit": "تم حفظ التعديل",
        })
        return context

    def post(self, request, *args, **kwargs):
        order = self.get_object()
        
        if int(request.POST["new_discount"]) != int(order.discount):
            update_discount(order, int(request.POST["new_discount"]))
            return HttpResponseRedirect(f"{order.id}")
        else:
            if order.total_order_price != Decimal(request.POST["total_order_price"]):
                order.update_total_prices(Decimal(request.POST["total_order_price"]))
            else:
                order_items = OrderItem.objects.filter(order=order)

                for order_item in order_items:
                    new_quantity = request.POST[f"quantity_{order_item}"]
                    try:
                        if int(new_quantity) < 1:
                            order_item.delete()
                        else:
                            order_item.quantity = Decimal(new_quantity)
                            order_item.save()
                    except ValueError:
                        order_item.delete()
                order.update_same_disc()
                update_items()

                if not OrderItem.objects.filter(order=order):
                    order.delete()
                    return HttpResponseRedirect("/users/")

            return HttpResponseRedirect(f"{order.id}")


# Helper functions (keeping the same as original)
def update_items():
    items = Item.objects.all()
    for item in items:
        item.update_item()

def get_order(order_id):
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return None
    return order

def get_coming_order(order_id):
    try:
        order = Store_Order.objects.get(id=order_id)
    except Store_Order.DoesNotExist:
        return None
    return order

def update_discount(order, new_discount):
    order.discount = new_discount
    order.save()
    order.update_same_disc()

def get_rest_info(customer):
    rest_orders = Order.objects.filter(customer=customer, is_fully_paid=False, is_used=True)
    rest_money_orders = rest_orders.values_list('rest_money', flat=True)
    if rest_money_orders.count() != 0:
        return {
            "count": rest_money_orders.count(),
            "rest_orders": rest_orders,
            "rest_money": sum(price for price in rest_money_orders)
            }

def get_total_orders_info(customer, year):
    if year == 0:
        total_money_orders = Order.objects.filter(customer=customer, is_used=True).values_list('total_order_price', flat=True)
        total_money = sum(price for price in total_money_orders)
        if total_money > 0:
            return sum(price for price in total_money_orders)
    else:
        if year == "all":
            total_orders = Order.objects.filter(customer=customer, is_used=True)
        else:  
            total_orders = Order.objects.filter(customer=customer, created_at__range=(datetime.date(year, 1, 1), datetime.date(year + 1, 1, 1)), is_used=True)
        total_money_orders = total_orders.values_list('total_order_price', flat=True)
        if total_money_orders.count() != 0:
            return {
                "count": total_money_orders.count(),
                "total_orders": total_orders,
                "total_money": sum(price for price in total_money_orders)
                }
    return None

def change_zone(date):
    return timezone.localtime(date)


# Additional views that need to be converted
class ChangeRestView(LoginRequiredMixin, TemplateView):
    template_name = "main/change_rest.html"
    login_url = "/login/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            order_id = int(self.request.GET.get("order_id"))
        except ValueError:
            context['err'] = "لا يمكن البحث عن طلب ب الاحرف او الرموز"
            return context

        order = get_order(order_id)
        if not order:
            return HttpResponseRedirect(f"/order_error/{order_id}")

        context['order'] = order
        return context

    def post(self, request, *args, **kwargs):
        try:
            order_id = int(request.GET.get("order_id"))
        except ValueError:
            return render(request, self.template_name, {
                "err": "لا يمكن البحث عن طلب ب الاحرف او الرموز"
            })

        order = get_order(order_id)
        if not order:
            return HttpResponseRedirect(f"/order_error/{order_id}")

        rest_money = request.POST["rest_money"]
        if order.rest_money - Decimal(rest_money) > Decimal(-1):
            order.rest_money -= Decimal(rest_money)
            order.save()
            return HttpResponseRedirect(f"/order_info/{order_id}")
        else:
            return render(request, self.template_name, {
                "order": order,
                "err": "لا يمكن اضافة قسط اعلي من قيمه الآجل"
            })


class PutRestView(LoginRequiredMixin, TemplateView):
    template_name = "main/put_rest.html"
    login_url = "/login/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            order_id = int(self.request.GET.get("order_id"))
        except ValueError:
            context['err'] = "لا يمكن البحث عن طلب ب الاحرف او الرموز"
            return context

        order = get_order(order_id)
        if not order:
            return HttpResponseRedirect(f"/order_error/{order_id}")

        context['order'] = order
        return context

    def post(self, request, *args, **kwargs):
        try:
            order_id = int(request.GET.get("order_id"))
        except ValueError:
            return render(request, self.template_name, {
                "err": "لا يمكن البحث عن طلب ب الاحرف او الرموز"
            })

        order = get_order(order_id)
        if not order:
            return HttpResponseRedirect(f"/order_error/{order_id}")

        rest = request.POST["rest_money"]
        order.rest_money = Decimal(rest)
        order.is_fully_paid = False
        order.save()

        return HttpResponseRedirect(f"/order_info/{order_id}")


class DeleteOrderView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = "main/delete_order.html"
    context_object_name = "order"
    pk_url_kwarg = "order_id"
    login_url = "/login/"

    def post(self, request, *args, **kwargs):
        order = self.get_object()
        customer_id = order.customer.id
        order.delete()
        update_items()
        return HttpResponseRedirect(f"/users/{customer_id}")


class DeleteOrderItemView(LoginRequiredMixin, View):
    login_url = "/login/"

    def get(self, request, order_item_id, *args, **kwargs):
        order_item = OrderItem.objects.get(pk=order_item_id)
        order_item.delete()
        update_items()

        order = Order.objects.get(pk=order_item.order.id)
        if not OrderItem.objects.filter(order=order):
            user_id = order.customer.id
            order.delete()
            return HttpResponseRedirect(f"/users/{user_id}")
        order.update_same_disc()
        return HttpResponseRedirect(f"/order_info/{order.id}")


class ChangeRankView(LoginRequiredMixin, View):
    login_url = "/login/"

    def get(self, request, order_id, *args, **kwargs):
        order = get_order(order_id)
        if not order:
            return HttpResponseRedirect(f"/order_error/{order_id}")
            
        if order.is_gomla:
            order.is_gomla = False
        else:
            order.is_gomla = True
        order.update_same_disc()
        for order_item in OrderItem.objects.filter(order=order):
            order_item.update_profit()

        return HttpResponseRedirect(f"/edit_order/{order_id}")


class OrderErrorView(LoginRequiredMixin, TemplateView):
    template_name = "main/error.html"
    login_url = "/login/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order_id = self.kwargs.get('order_id')
        order = get_order(order_id)
        if not order:
            context.update({
                "message": f"الطلب رقم {order_id} غير موجود",
                "message2": "البحث عن طلب اخر",
            })
        else:
            return HttpResponseRedirect(f"/order_info/{order.id}")
        return context


class UsersSearchView(LoginRequiredMixin, View):
    login_url = "/login/"

    def get(self, request, text, *args, **kwargs):
        if text.isnumeric():
            text = int(text)
            if text % 10 == 0:
                customers = Customer.objects.filter(id__range=(text, text + 10))
            else:
                customers = Customer.objects.filter(id__contains=text)
        else:
            customers = Customer.objects.filter(name__contains=f"{text}")
        return JsonResponse([customer.serialize() for customer in customers], safe=False)


class CreateItemView(LoginRequiredMixin, TemplateView):
    template_name = "main/create_item.html"
    login_url = "/login/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "form": ItemForm(),
            "category_form": CategoryForm(),
        })
        return context

    def post(self, request, *args, **kwargs):
        form = ItemForm(request.POST)
        if form.is_valid():
            category = form.cleaned_data['category']
            name = form.cleaned_data['name']
            real_price = form.cleaned_data['real_price']
            gomla_price = form.cleaned_data['gomla_price']
            market_price = form.cleaned_data['market_price']
            stock_quantity = form.cleaned_data['stock_quantity']
            Item.objects.create(category=category, name=name, real_price=real_price, gomla_price=gomla_price, stock_quantity=stock_quantity, market_price=market_price)

            return render(request, self.template_name, {
                "form": ItemForm(),
                "category_form": CategoryForm(),
                "success_message": f"بنجاح - {name} - تم أضافة المنتج "
            })
        else:
            return render(request, self.template_name, {
                "form": ItemForm(),
                "category_form": CategoryForm(),
                "err_message": "حدث خطأ في تسجيل المنتج من الممكن تشابه الاسم مع اخر موجود بالفعل",
            })


class CreateCategoryView(LoginRequiredMixin, View):
    login_url = "/login/"

    def post(self, request, *args, **kwargs):
        category_form = CategoryForm(request.POST)
        if category_form.is_valid():
            category_name = category_form.cleaned_data['name']
            Category.objects.create(name=category_name)

            return render(request, "main/create_item.html", {
                "form": ItemForm(),
                "category_form": CategoryForm(),
                "success_message": f"بنجاح - {category_name} - تم أضافة النوع "
            })
        else:
            return render(request, "main/create_item.html", {
                "form": ItemForm(),
                "category_form": CategoryForm(),
                "err_message": "حدث خطأ في تسجيل النوع من الممكن تشابه الاسم مع اخر موجود بالفعل",
            })


class CreateCustomerView(LoginRequiredMixin, TemplateView):
    template_name = "main/create_customer.html"
    login_url = "/login/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CustomerForm()
        return context

    def post(self, request, *args, **kwargs):
        form = CustomerForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            number = form.cleaned_data['number']
            is_supplier = form.cleaned_data['is_supplier']
            Customer.objects.create(name=name, number=number, is_supplier=is_supplier)

            return render(request, self.template_name, {
                "form": CustomerForm(),
                "success_message": f"بنجاح - {name} - تم أضافة العميل "                
            })
        else:
            return render(request, self.template_name, {
                "form": form,
                "err_message": "حدث خطأ في تسجيل العميل من الممكن تشابه الرقم مع اخر موجود بالفعل",
            })




class UpdateItemView(LoginRequiredMixin, DetailView):
    model = Item
    template_name = "main/update_item.html"
    context_object_name = "item"
    pk_url_kwarg = "item_id"
    login_url = "/login/"

    def post(self, request, *args, **kwargs):
        item = self.get_object()
        try:
            name = request.POST["name"]
            real_price = request.POST["real_price"]
            gomla_price = request.POST["gomla_price"]
            market_price = request.POST["market_price"]
            item.name = name
            item.real_price = Decimal(real_price)
            item.gomla_price = Decimal(gomla_price)
            item.market_price = Decimal(market_price)
            item.save()
            return render(request, self.template_name, {
                "item": item,
                "success_message": "تم حفظ تعديلك بنجاح ",
            })
        except:
            return render(request, self.template_name, {
                "item": item,
                "err_message": "حدث خطأ في تحديث بيانات المنتج ",
            })


# Placeholder functions for views that haven't been converted yet
@login_required(login_url="/login/")
def total_orders(request):
    if request.method == 'GET':
        all_orders = Order.objects.filter(is_used=True).order_by("created_at")
        all_duration = {}
        years_info = {}
        all_coming_date = Store_Order.objects.all().order_by("created_at").values_list('created_at', flat=True)
        
        for order in all_orders:
            order_time = timezone.localtime(order.created_at)

            if not str(order_time.year) in all_duration.keys():
                all_duration[f"{order_time.year}"] = {}
            if not str(order_time.month) in all_duration[f"{order_time.year}"].keys():
                all_duration[f"{order_time.year}"][f"{order_time.month}"] = get_totalsales_formonth(order.created_at.year, order.created_at.month)

        years_sales = {}
        years_profit = {}
        years_averages = {}
        
        for year in all_duration.keys():
            year = int(year)
            years_info[f"{year}"] = get_sales_per_year(year, all_duration[f"{year}"].keys())
            year_order = Order.objects.filter(created_at__range=(datetime.date(year, 1, 1), datetime.date(year + 1, 1, 1)), is_used=True)
            year_count = year_order.count()
            years_sales[year] = sum(order_price for order_price in year_order.values_list("total_order_price", flat=True))
            years_profit[year] = sum(order_price for order_price in year_order.values_list("profit", flat=True))
            years_averages[year] = round(years_sales[year] / year_count, 2) if year_count > 0 else 0

        years_info = dict(sorted(years_info.items(), key=lambda x: int(x[0]), reverse=True))
        years_list = list(years_info.keys())

        order_count = all_orders.count()
        orders_sales = sum(order_price for order_price in all_orders.values_list("total_order_price", flat=True))
        average_order = round(orders_sales / order_count, 2) if order_count > 0 else 0
        total_profits = all_orders.values_list("profit", flat=True)
        total_profit = sum(profit for profit in total_profits)
        rest_moneys = all_orders.values_list("rest_money", flat=True)
        rest_money = sum(rest for rest in rest_moneys)

        all_data = {
            "order_count": order_count,
            "orders_sales": orders_sales,
            "average_order": average_order,
            "total_profit": total_profit,
            "rest_money": rest_money,
            "years_sales": years_sales,
            "years_profit": years_profit,
            "years_averages": years_averages,
        }
        
        return render(request, "main/sales.html", {
            "years_info": years_info,
            "years_list": years_list,
            "all_data": all_data,
        })

@login_required(login_url="/login/")
def month_sales(request):
    arabic_months = {
        1: "يناير",
        2: "فبراير",
        3: "مارس",
        4: "أبريل",
        5: "مايو",
        6: "يونيو",
        7: "يوليو",
        8: "أغسطس",
        9: "سبتمبر",
        10: "أكتوبر",
        11: "نوفمبر",
        12: "ديسمبر"
    }

    try:
        year = int(request.GET.get("y"))
        month = int(request.GET.get("m"))
        month_data = get_totalsales_formonth(year, month)
        shahr = arabic_months.get(month, None)
        
        # Get the actual order objects for the template
        start_date = datetime.date(year, month, 1)
        if month == 12:
            end_date = datetime.date(year + 1, 1, 1)
        else:
            end_date = datetime.date(year, month + 1, 1)
            
        orders = Order.objects.filter(created_at__range=(start_date, end_date), is_used=True).order_by("-created_at")
        coming_orders = Store_Order.objects.filter(created_at__range=(start_date, end_date)).order_by("-created_at")
        
        # Add the actual order objects to month_data
        month_data["orders"] = orders
        month_data["coming_orders"] = coming_orders
        
    except ValueError:
        return HttpResponse("error: خطأ في ادخال الشهر او السنة.")

    month_char_data = {
        "مبيعات الشهر": month_data["orders_sales"],
        "لم يتم سداده بعد": month_data["debt"],
        "مصاريف طلبيات": month_data["coming_sales"],
    }
    debt_char_data = {
        "الربح": month_data["profit"],
        "مستحق للطلبيات": month_data["coming_debt"],
    }
    return render(request, "main/month_sales.html", {
        "month_data": month_data,
        "shahr": shahr,
        "year": year,
        "debt_char_data": debt_char_data,
        "month_char_data": month_char_data,
    })

@login_required(login_url="/login/")
def coming_order(request):
    items_object = {}
    categories = Category.objects.all()
    suppliers = Customer.objects.filter(is_supplier=True)
    for category in categories:
        items = Item.objects.filter(category=category).order_by('id')
        items_object[f"{category.name}"] = items

    if request.method == 'GET':
        customers = Customer.objects.filter(is_shop=True)
        return render(request, "main/create_store_order.html", {
            "items_object": items_object,
            "customers": customers,
            "suppliers": suppliers,
        })
        
    else:
        customer_id = request.POST["customer"]
        supplier_id = request.POST["supplier"]
        customer = Customer.objects.get(id=customer_id)
        supplier = Customer.objects.get(id=supplier_id)

        check_order = False
        order = Store_Order.objects.create(customer=customer, supplier=supplier)
        
        for category in items_object.values():
            for item in category:
                try:
                    quantity = int(request.POST[f"quantity_{item.id}"])
                except ValueError:
                    quantity = 0
                if quantity > 0:
                    Store_OrderItem.objects.create(
                        order=order, item=item, quantity=quantity, single_real_price=item.real_price,
                        single_gomla_price=item.gomla_price, single_market_price=item.market_price
                    )
                    check_order = True

        if check_order == False:
            order.delete()
            return HttpResponseRedirect("/coming_order")

        last_order = Store_Order.objects.all().exclude(id=order.id).order_by("-id").first()
        if last_order:
            last_order.is_done = True
            last_order.save()
        return HttpResponseRedirect(f"/coming_order/{order.id}")

def add_coming_items(request, order_id):
    # This will be converted later
    pass

@login_required(login_url="/login/")
def coming_order_info(request, order_id):
    order = get_object_or_404(Store_Order, pk=order_id)
    order_items = Store_OrderItem.objects.filter(order=order)
    return render(request, "main/coming_order_info.html", {
        "order": order,
        "order_items": order_items,
    })

def delete_coming_item(request, item_id):
    # This will be converted later
    pass

def edit_coming_item(request, item_id):
    # This will be converted later
    pass

def delete_coming_order(request, order_id):
    # This will be converted later
    pass

def done_coming_order(request, order_id):
    # This will be converted later
    pass

def store_coming_info(request, store_id):
    # This will be converted later
    pass

def supplier_coming_info(request, supplier_id):
    # This will be converted later
    pass

@login_required(login_url="/login/")
def all_rest_orders(request):
    orders = {}
    customers = Customer.objects.all().order_by('-is_shop', '-name')
    for customer in customers:
        customer_rest = customer.orders.filter(is_fully_paid=False).order_by('created_at')
        if customer_rest.count() > 0:
            orders[customer] = customer_rest
    return render(request, "main/all_rest_orders.html", {
        "orders": orders,
    })

def all_rest_coming_orders(request):
    # This will be converted later
    pass

# Helper functions
def get_sales_per_year(year, months):
    orders = Order.objects.filter(created_at__range=(datetime.date(year, 1, 1), datetime.date(year + 1, 1, 1)), is_used=True).order_by("created_at")
    coming_orders = Store_Order.objects.filter(created_at__range=(datetime.date(year, 1, 1), datetime.date(year + 1, 1, 1)))
    order_count = orders.count()

    orders_sales = sum(orders.values_list("total_order_price", flat=True))
    coming_sales = sum(coming_orders.values_list("total_order_price", flat=True))
    average_order = round(orders_sales / order_count, 2) if order_count > 0 else 0
    profit = sum(orders.values_list("profit", flat=True))
    debt = sum(orders.values_list("rest_money", flat=True))
    coming_debt = sum(coming_orders.values_list("rest_money", flat=True))

    months_sales = {}
    for month in months:
        months_sales[month] = (get_totalsales_formonth(year, int(month)))

    year_result = {
        "order_count": order_count, 
        "orders_sales": orders_sales, 
        "profit": profit, 
        "debt": debt, 
        "average_order": average_order,
        "orders": orders,
        "months_sales": months_sales, 
        "months": months, 
        "coming_sales": coming_sales, 
        "coming_debt": coming_debt, 
    }
    return year_result

def get_totalsales_formonth(year, month):
    start_date = datetime.date(year, month, 1)

    if month == 12:
        end_date = datetime.date(year + 1, 1, 1)
    else:
        end_date = datetime.date(year, month + 1, 1)

    orders = Order.objects.filter(created_at__range=(start_date, end_date), is_used=True)
    coming_orders = Store_Order.objects.filter(created_at__range=(start_date, end_date))

    order_count = orders.count()
    orders_sales = sum(orders.values_list("total_order_price", flat=True))
    coming_sales = sum(coming_orders.values_list("total_order_price", flat=True))
    average_order = round(orders_sales / order_count, 2) if order_count > 0 else 0
    profit = sum(orders.values_list("profit", flat=True))
    debt = sum(orders.values_list("rest_money", flat=True))
    coming_debt = sum(coming_orders.values_list("rest_money", flat=True))

    month_result = {
        "order_count": order_count,
        "orders_sales": orders_sales,
        "coming_sales": coming_sales,
        "average_order": average_order,
        "profit": profit,
        "debt": debt,
        "coming_debt": coming_debt,
    }
    return month_result

def coming_change_rest(request):
    # This will be converted later
    pass

def coming_put_rest(request):
    # This will be converted later
    pass


# Management Views for Categories and Items
class CategoryManagementView(LoginRequiredMixin, TemplateView):
    template_name = "main/category_management.html"
    login_url = "/login/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = Category.objects.all().order_by('name')
        
        # Get usage statistics for each category
        category_stats = []
        for category in categories:
            items_count = Item.objects.filter(category=category).count()
            used_items_count = Item.objects.filter(category=category, used_quantity__gt=0).count()
            total_orders = OrderItem.objects.filter(item__category=category).count()
            
            category_stats.append({
                'category': category,
                'items_count': items_count,
                'used_items_count': used_items_count,
                'total_orders': total_orders,
                'can_delete': items_count == 0  # Can only delete if no items
            })
        
        context.update({
            "category_stats": category_stats,
            "form": CategoryForm(),
        })
        return context

    def post(self, request, *args, **kwargs):
        form = CategoryForm(request.POST)
        if form.is_valid():
            category_name = form.cleaned_data['name']
            Category.objects.create(name=category_name)
            return HttpResponseRedirect(request.path)
        else:
            return render(request, self.template_name, {
                "category_stats": self.get_context_data()["category_stats"],
                "form": form,
                "err_message": "حدث خطأ في تسجيل النوع من الممكن تشابه الاسم مع اخر موجود بالفعل",
            })


class ItemManagementView(LoginRequiredMixin, TemplateView):
    template_name = "main/item_management.html"
    login_url = "/login/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        items = Item.objects.all().order_by('category__name', 'name')
        
        # Get usage statistics for each item
        item_stats = []
        for item in items:
            total_orders = OrderItem.objects.filter(item=item).count()
            total_quantity_sold = OrderItem.objects.filter(item=item).aggregate(
                total=Sum('quantity')
            )['total'] or 0
            
            item_stats.append({
                'item': item,
                'total_orders': total_orders,
                'total_quantity_sold': total_quantity_sold,
                'can_delete': total_orders == 0  # Can only delete if never used in orders
            })
        
        context.update({
            "item_stats": item_stats,
            "form": ItemForm(),
            "categories": Category.objects.all().order_by('name'),
        })
        return context

    def post(self, request, *args, **kwargs):
        form = ItemForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(request.path)
        else:
            return render(request, self.template_name, {
                "item_stats": self.get_context_data()["item_stats"],
                "form": form,
                "categories": Category.objects.all().order_by('name'),
                "err_message": "حدث خطأ في تسجيل المنتج من الممكن تشابه الاسم مع اخر موجود بالفعل",
            })


class DeleteCategoryView(LoginRequiredMixin, View):
    login_url = "/login/"

    def post(self, request, category_id, *args, **kwargs):
        try:
            category = Category.objects.get(id=category_id)
            items_count = Item.objects.filter(category=category).count()
            
            if items_count > 0:
                return JsonResponse({
                    'success': False,
                    'message': f'لا يمكن حذف النوع "{category.name}" لأنه يحتوي على {items_count} منتج'
                })
            
            category_name = category.name
            category.delete()
            
            return JsonResponse({
                'success': True,
                'message': f'تم حذف النوع "{category_name}" بنجاح'
            })
        except Category.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'النوع غير موجود'
            })


class DeleteItemView(LoginRequiredMixin, View):
    login_url = "/login/"

    def post(self, request, item_id, *args, **kwargs):
        try:
            item = Item.objects.get(id=item_id)
            total_orders = OrderItem.objects.filter(item=item).count()
            
            if total_orders > 0:
                return JsonResponse({
                    'success': False,
                    'message': f'لا يمكن حذف المنتج "{item.name}" لأنه مستخدم في {total_orders} طلب'
                })
            
            item_name = item.name
            item.delete()
            
            return JsonResponse({
                'success': True,
                'message': f'تم حذف المنتج "{item_name}" بنجاح'
            })
        except Item.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'المنتج غير موجود'
            })


class UpdateCategoryView(LoginRequiredMixin, View):
    login_url = "/login/"

    def post(self, request, category_id, *args, **kwargs):
        try:
            category = Category.objects.get(id=category_id)
            new_name = request.POST.get('name', '').strip()
            
            if not new_name:
                return JsonResponse({
                    'success': False,
                    'message': 'اسم النوع لا يمكن أن يكون فارغاً'
                })
            
            # Check if name already exists
            if Category.objects.filter(name=new_name).exclude(id=category_id).exists():
                return JsonResponse({
                    'success': False,
                    'message': 'اسم النوع موجود بالفعل'
                })
            
            old_name = category.name
            category.name = new_name
            category.save()
            
            return JsonResponse({
                'success': True,
                'message': f'تم تحديث النوع من "{old_name}" إلى "{new_name}" بنجاح'
            })
        except Category.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'النوع غير موجود'
            })


class UpdateItemView(LoginRequiredMixin, View):
    login_url = "/login/"

    def post(self, request, item_id, *args, **kwargs):
        try:
            item = Item.objects.get(id=item_id)
            
            # Get form data
            name = request.POST.get('name', '').strip()
            category_id = request.POST.get('category')
            real_price = request.POST.get('real_price')
            gomla_price = request.POST.get('gomla_price')
            market_price = request.POST.get('market_price')
            stock_quantity = request.POST.get('stock_quantity')
            
            # Validate required fields
            if not name or not category_id:
                return JsonResponse({
                    'success': False,
                    'message': 'جميع الحقول مطلوبة'
                })
            
            # Check if name already exists
            if Item.objects.filter(name=name).exclude(id=item_id).exists():
                return JsonResponse({
                    'success': False,
                    'message': 'اسم المنتج موجود بالفعل'
                })
            
            # Validate prices
            try:
                real_price = Decimal(real_price) if real_price else Decimal('0')
                gomla_price = Decimal(gomla_price) if gomla_price else Decimal('0')
                market_price = Decimal(market_price) if market_price else Decimal('0')
                stock_quantity = int(stock_quantity) if stock_quantity else 0
            except (ValueError, InvalidOperation):
                return JsonResponse({
                    'success': False,
                    'message': 'قيم الأسعار أو الكمية غير صحيحة'
                })
            
            # Get category
            try:
                category = Category.objects.get(id=category_id)
            except Category.DoesNotExist:
                return JsonResponse({
                    'success': False,
                    'message': 'النوع المحدد غير موجود'
                })
            
            # Update item
            item.name = name
            item.category = category
            item.real_price = real_price
            item.gomla_price = gomla_price
            item.market_price = market_price
            item.stock_quantity = stock_quantity
            item.save()
            
            return JsonResponse({
                'success': True,
                'message': f'تم تحديث المنتج "{item.name}" بنجاح'
            })
        except Item.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'المنتج غير موجود'
            })
