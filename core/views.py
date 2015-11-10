from django.shortcuts import render
from django.views.generic import TemplateView, CreateView, ListView, DetailView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from .models import *
# Create your views here.
class Home(TemplateView):
    template_name = "home.html"

class PostCreateView(CreateView):
    model = Post
    template_name = "post/post_form.html"
    fields = ['title', 'description']
    success_url = reverse_lazy('post_list')

    def form_valid(self, form):
      form.instance.user = self.request.user
      return super(PostCreateView, self).form_valid(form)

class PostListView(ListView):
    model = Post
    template_name = "post/post_list.html"

class PostDetailView(DetailView):
    model = Post
    template_name = 'post/post_detail.html'

class PostUpdateView(UpdateView):
    model = Post
    template_name = 'post/post_form.html'
    fields = ['title', 'description']

class PostDeleteView(DeleteView):
    model = Post
    template_name = 'post/post_confirm_delete.html'
    success_url = reverse_lazy('post_list')