from django.http import HttpResponse
from django.shortcuts import render
from catalog.models import Product, Category
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy


class ProductListView(ListView):
    model = Product
    template_name = 'catalog/products_list.html'  # Имя шаблона для отображения списка продуктов
    context_object_name = 'products'


class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'


class ContactTemplateView(TemplateView):
    template_name = 'catalog/contacts.html'

    def get_context_data(self, **kwargs):
        if self.request.method == 'POST':
            name = self.request.POST.get('name')
            phone = self.request.POST.get('phone')
            message = self.request.POST.get('message')
            print(name)
            print(phone)
            print(message)
            return HttpResponse('Сообщение отправлено!')


class ProductCreateView(CreateView):
    model = Product
    fields = ['name', 'description', 'price', 'category', 'image']
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:products_list')


class ProductUpdateView(UpdateView):
    model = Product
    fields = ['name', 'description', 'price', 'category', 'image']
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:products_list')


class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'catalog/product_delete_confirm.html'
    success_url = reverse_lazy('catalog:products_list')
    context_object_name = 'product'

