from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from pytils.translit import slugify
from blog.services import send_mail_for100

from blog.models import Blog


class BlogListView(ListView):
    model = Blog

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(is_active=True)
        return queryset


class BlogDetailView(LoginRequiredMixin, DetailView):
    model = Blog

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        obj = self.object.save()
        if self.object.views_count == 100:
            send_mail_for100(self.object.id)
        return self.object


class BlogCreateView(LoginRequiredMixin, CreateView):
    model = Blog
    fields = ('topic', 'image', 'message',)
    success_url = reverse_lazy('blog:main')

    def form_valid(self, form):
        if form.is_valid():
            new_blog = form.save()
            new_blog.slug = slugify(new_blog.topic)
            new_blog.owner = self.request.user
            new_blog.save()

        return super().form_valid(form)


class BlogUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Blog
    fields = ('topic', 'image', 'message', 'is_active')

    def test_func(self):
        permi = ('blog.change_blog',)
        _user = self.request.user
        _instance = self.get_object()
        if _user == _instance.owner or _user.has_perms(permi):
            return True
        return self.handle_no_permission()

    def get_success_url(self):
        return reverse('blog:detail', args=[self.kwargs.get('pk')])

    def form_valid(self, form):
        if form.is_valid():
            new_blog = form.save()
            new_blog.slug = slugify(new_blog.topic)
            new_blog.save()

        return super().form_valid(form)


class BlogDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Blog
    success_url = reverse_lazy('blog:main')

    def test_func(self):
        permi = ('blog.delete_blog',)
        _user = self.request.user
        _instance = self.get_object()
        if _user == _instance.owner or _user.has_perms(permi):
            return True
        return self.handle_no_permission()
