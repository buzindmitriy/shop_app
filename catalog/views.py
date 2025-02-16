from django.core.cache import cache
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from catalog.forms import ProductForm, ProductModeratorForm
from catalog.models import Product, Category
from django.views.generic import (
    ListView,
    DetailView,
    TemplateView,
    CreateView,
    UpdateView,
    DeleteView, View
)
from django.urls import reverse_lazy, reverse

from catalog.services import CategoryService


class ProductListView(ListView):
    model = Product
    template_name = (
        "catalog/products_list.html"  # Имя шаблона для отображения списка продуктов
    )
    context_object_name = "products"

    def get_queryset(self):
        # Проверка наличия кэша
        cached_products = cache.get("products")
        if cached_products:
            return cached_products
        # Если кэша нет, получаем объекты из базы и кешируем их
        products = Product.objects.all()
        cache.set("products", products, 60 * 5)
        user = self.request.user
        if user.has_perm("catalog.can_unpublish_product"):
            return Product.objects.all()
        return Product.objects.filter(is_publish=True)


@method_decorator(cache_page(60 * 5), name='dispatch')
class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = "catalog/product_detail.html"
    context_object_name = "product"


class ContactTemplateView(LoginRequiredMixin, TemplateView):
    template_name = "catalog/contacts.html"
    login_url = reverse_lazy("users:login")

    def get_context_data(self, **kwargs):
        if self.request.method == "POST":
            name = self.request.POST.get("name")
            phone = self.request.POST.get("phone")
            message = self.request.POST.get("message")
            print(name)
            print(phone)
            print(message)
            return HttpResponse("Сообщение отправлено!")


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"
    login_url = reverse_lazy("users:login")
    success_url = reverse_lazy("catalog:products_list")

    def form_valid(self, form):
        product = form.save(commit=False)
        product.owner = self.request.user
        product.save()
        return redirect(reverse("catalog:products_list"))


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"
    login_url = reverse_lazy("users:login")
    success_url = reverse_lazy("catalog:products_list")

    def get_form_class(self):
        user = self.request.user
        if user == self.object.owner:
            return ProductForm
        elif user.has_perm("catalog.can_unpublish_product"):
            return ProductModeratorForm


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = "catalog/product_delete_confirm.html"
    login_url = reverse_lazy("users:login")
    success_url = reverse_lazy("catalog:products_list")
    context_object_name = "product"

    def post(self, request, pk):
        product = get_object_or_404(Product, id=pk)
        if request.user == product.owner or request.user.has_perm("catalog.can_delete_product"):
            product.delete()
            return redirect(reverse("catalog:products_list"))
        else:
            return HttpResponseForbidden("У Вас нет прав на удаление продукта!")


class CategoryListView(ListView):
    model = Category
    template_name = "catalog/categories_list.html"
    context_object_name = "categories"


class CategoryDetailView(DetailView):
    model = Category
    template_name = "catalog/category_detail.html"
    context_object_name = "category"

    def get_context_data(self, **kwargs):
        # Получаем объекты продуктов и категории
        products = CategoryService.get_products_from_category(category=self.object)
        categories = CategoryService.get_all_categories()
        return super().get_context_data(products=products, categories=categories, **kwargs)
