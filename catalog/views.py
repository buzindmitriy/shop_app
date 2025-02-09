from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from catalog.models import Product, Category


def products_list(request):
    products = Product.objects.all()
    context = {"products": products}
    return render(request, "products_list.html", context)


def products_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    context = {"product": product}
    return render(request, 'products_detail.html', context)


def contact_us(request):
    if request.method == "POST":
        # Получение данных из формы
        name = request.POST.get("name")
        message = request.POST.get("message")
        # Обработка данных (например, сохранение в БД, отправка email и т. д.)
        print(name)
        print(message)
        # Здесь мы просто возвращаем простой ответ
        return HttpResponse(f"Спасибо, {name}! Ваше сообщение получено.")
    return render(request, "contacts.html")


def add_product(request):
    if request.method == 'POST':
        # Получение данных из формы
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        category_id = request.POST.get('category')
        image = request.FILES.get('image')  # Загрузка изображения продукта (если оно есть)
        # Создание нового продукта
        product = Product.objects.create(
            name=name,
            description=description,
            price=price,
            category_id=category_id,
            image=image,
        )
        return HttpResponse(f"Продукт '{product.name}' успешно добавлен.")
    # Формирование формы добавления продукта
    categories = Category.objects.all()
    return render(request, 'add_product.html', {'categories': categories})
