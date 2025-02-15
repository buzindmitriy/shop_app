from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import get_object_or_404, redirect

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


class ProductListView(ListView):
    model = Product
    template_name = (
        "catalog/products_list.html"  # Имя шаблона для отображения списка продуктов
    )
    context_object_name = "products"

    def get_queryset(self):  # фильтрация продуктов по опубликованным
        user = self.request.user
        if user.has_perm("catalog.can_unpublish_product"):
            return Product.objects.all()
        return Product.objects.filter(is_publish=True)


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
