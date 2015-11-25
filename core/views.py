from django.shortcuts import render
from django.views.generic import TemplateView, CreateView, ListView, DetailView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from django.core.exceptions import PermissionDenied
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

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        post = Post.objects.get(id=self.kwargs['pk'])
        comment = Comment.objects.filter(post=post)
        context['post'] = post
        user_comment = Comment.objects.filter(post=post, user=self.request.user)
        context['user_comment'] = user_comment
        return context

class PostUpdateView(UpdateView):
      model = Post
      template_name = 'post/post_form.html'
      fields = ['title', 'description']

      def get_object(self, *args, **kwargs):
              object = super(PostUpdateView, self).get_object(*args, **kwargs)
              if object.user != self.request.user:
                  raise PermissionDenied()
              return object

class PostDeleteView(DeleteView):
      model = Post
      template_name = 'post/post_confirm_delete.html'
      success_url = reverse_lazy('post_list')

      def get_object(self, *args, **kwargs):
              object = super(PostDeleteView, self).get_object(*args, **kwargs)
              if object.user != self.request.user:
                  raise PermissionDenied()
              return object

class CommentCreateView(CreateView):
      model = Comment
      template_name = "post/post_form.html"
      fields = ['text']

      def get_success_url(self):
          return self.object.post.get_absolute_url()

      def form_valid(self, form):
          post = Post.objects.get(id=self.kwargs['pk'])
          if Comment.objects.filter(post=post, user=self.request.user).exists():
              raise PermissionDenied()
          form.instance.user = self.request.user
          form.instance.post = Post.objects.get(id=self.kwargs['pk'])
          return super(CommentCreateView, self).form_valid(form)

class CommentUpdateView(UpdateView):
          model = Comment
          pk_url_kwarg = 'comment_pk'
          template_name = 'comment/comment_form.html'
          fields = ['text']

          def get_success_url(self):
            return self.object.post.get_absolute_url()

          def get_object(self, *args, **kwargs):
                  object = super(CommentUpdateView, self).get_object(*args, **kwargs)
                  if object.user != self.request.user:
                      raise PermissionDenied()
                  return object

class CommentDeleteView(DeleteView):
    model = Comment
    pk_url_kwarg = 'comment_pk'
    template_name = 'comment/comment_confirm_delete.html'

    def get_success_url(self):
        return self.object.post.get_absolute_url()

    def get_object(self, *args, **kwargs):
            object = super(CommentDeleteView, self).get_object(*args, **kwargs)
            if object.user != self.request.user:
                raise PermissionDenied()
            return object
