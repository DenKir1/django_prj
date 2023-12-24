
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.forms import inlineformset_factory
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView


from catalog.forms import StyleFormMixin
from config import settings
from users.forms import UserRegisterForm, UserProfileForm, VerifyForm
from users.models import User, Verify


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):

        new_user = form.save(commit=False)
        new_user.save()

        verify_code = User.objects.make_random_password(length=15)

        verify_ = Verify(user_id=new_user.pk, verify_code=verify_code)
        verify_.save()

        send_mail(
            subject='Подтверждение регистрации',
            message=f' Введите код верификации: {verify_code}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[new_user.email]
        )
        print(f'{new_user} Введите код верификации: {verify_code}')
        return super().form_valid(form)


class ProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        UserFormset = inlineformset_factory(User, Verify, form=VerifyForm, extra=0)
        if self.request.method == 'POST':
            context_data['formset'] = UserFormset(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = UserFormset(instance=self.object)

        return context_data

    def form_valid(self, form):
        formset = self.get_context_data()['formset']
        self.object = form.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()
        verify_user = self.object

        verify_pass = verify_user.verify_set.all()[0].verify_pass
        verify_code = verify_user.verify_set.all()[0].verify_code
        #print(verify_pass)
        #print(verify_code)
        if not verify_user.is_verify:
            if verify_code == verify_pass:
                verify_user.is_verify = True
                verify_user.save()
                print('Верификация прошла успешно')
        return super().form_valid(form)


def get_password(request):
    new_pass = User.objects.make_random_password(length=15)
    send_mail(
        subject='Новый пароль',
        message=f'Новый пароль {new_pass}',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[request.user.email]
    )
    request.user.set_password(new_pass)
    request.user.save()
    print(f'{request.user.email} - получил новый пароль - {new_pass}')
    return redirect(reverse('users:login'))
