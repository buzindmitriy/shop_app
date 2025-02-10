import secrets

from django.shortcuts import get_object_or_404, redirect

from config.settings import EMAIL_HOST_USER
from django.core.mail import send_mail
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView
from .forms import CustomUserRegistrationForm
from .models import User


class RegisterView(CreateView):
    model = User
    form_class = CustomUserRegistrationForm
    success_url = reverse_lazy('catalog:products_list')
    template_name = 'users/register.html'

    def form_valid(self, form):
        user = form.save()
        user.is_active = False  # Ставим флаг активности на False для пользователя до подтверждения регистрации
        self.send_verification_email(user)  # Отправка подтверждения регистрации
        self.send_welcome_email(user.email)  # отправка приветственного письма

    def send_welcome_email(self, user_email):  # отправка приветственного письма
        subject = 'Добро пожаловать в наш сервис'
        message = 'Спасибо, что зарегистрировались в нашем сервисе!'
        from_email = EMAIL_HOST_USER
        recipient_list = [user_email]
        send_mail(subject, message, from_email, recipient_list)

    def send_verification_email(self, user):
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f'http://{host}/users/email-confirm/{token}/'
        send_mail(
            subject='Подтверждение регистрации',
            message=f'Для подтверждения регистрации перейдите по ссылке: {url}',
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email],
        )
        return super().form_valid(form)


def email_verification(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse('users:login'))
