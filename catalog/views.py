from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from catalog.forms import ProductForm
from catalog.models import Product, Category
from django.views.generic import (
    ListView,
    DetailView,
    TemplateView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.urls import reverse_lazy


class ProductListView(ListView):
    model = Product
    template_name = (
        "catalog/products_list.html"  # Имя шаблона для отображения списка продуктов
    )
    context_object_name = "products"


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


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"
    login_url = reverse_lazy("users:login")
    success_url = reverse_lazy("catalog:products_list")


class ProductDeleteView(DeleteView):
    model = Product
    template_name = "catalog/product_delete_confirm.html"
    success_url = reverse_lazy("catalog:products_list")
    context_object_name = "product"
