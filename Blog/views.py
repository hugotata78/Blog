from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView, DetailView,View
from django.db.models import Q
from django.urls import reverse
from django.views.generic import FormView
from django.views.generic.detail import SingleObjectMixin
from django.contrib.auth.mixins import LoginRequiredMixin

from . models import Post, Category, Comment
from . forms import PostCommentForm

# Create your views here.

def order_post(query):
    if query == '-created_at':
        return 'Recientes'
    if query == 'created_at':
        return 'Antiguos'
    if query == 'title':
        return 'Títulos (A-Z)'
    if query == '-title':
        return 'Títulos (Z-A)'

class HomePageView(ListView):
    model = Post
    template_name = 'blog/home_page.html'

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        context['featured'] = Post.objects.filter(featured=True)[:3]
        context['recent'] = Post.objects.all()[:3]
        context['categories'] = Category.objects.all()
        return context

class PostListView(ListView):
    model = Post
    template_name = 'blog/results.html'
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super(PostListView, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['info_title'] = 'Blog > Todos los Artículos'
        return context

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['form'] = PostCommentForm()
        return context

class PostCommentFormView(LoginRequiredMixin, SingleObjectMixin, FormView):
    template_name = 'blog/post_detail.html'
    form_class = PostCommentForm
    model = Post

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        f = form.save(commit=False)
        f.author = self.request.user
        f.post = self.object
        f.save()
        return super().form_valid(form)
        
    def get_success_url(self):
        return reverse('blog:post', kwargs={'slug': self.object.slug}) + '#comments-section'

class PostView(View):

    def get(self, request, *args, **kwargs):
        view = PostDetailView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = PostCommentFormView.as_view()
        return view(request, *args, **kwargs)

class FeaturedPostListView(ListView):
    model = Post
    template_name = 'blog/results.html'
    paginate_by = 3

    def get_queryset(self):
        query = Post.objects.filter(featured=True)
        return query
    
    def get_context_data(self, **kwargs):
        context = super(FeaturedPostListView, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['info_title'] = 'Blog > Destacados'
        return context

class CategoryListView(ListView):
    model = Post
    template_name = 'blog/results.html'
    paginate_by = 3

    def get_queryset(self):
        query = self.request.path.replace('/category/', '')
        post_list = Post.objects.filter(categories__slug=query)
        return post_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = Category.objects.filter(slug=self.kwargs['slug'])
        context['categories'] = Category.objects.all()
        context['info_title'] = f'Blog > Categoría > {category[0].title}'
        return context


class SearchResultsView(ListView):
    model = Post
    template_name = 'blog/results.html'
    paginate_by = 3

    def get_queryset(self):
        query = self.request.GET.get('search')
        post_list = Post.objects.filter(
            Q(title__icontains=query) | Q(categories__title__icontains=query)
        ).distinct()
        return post_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('search')
        context['query'] = self.request.GET.get('search')
        context['categories'] = Category.objects.all()
        context['info_title'] = f'Blog > busqueda > {query} '
        return context

class SortListView(ListView):
    model = Post
    template_name = 'blog/results.html'
    paginate_by = 3

    def get_queryset(self):
        query = self.request.path.replace('/order/','')
        post_list = Post.objects.all().order_by(query)
        return post_list
    def get_context_data(self, **kwargs):
        context = super(SortListView,self).get_context_data(**kwargs)
        query = self.request.path.replace('/order/','')
        order = order_post(query)
        context['categoties'] = Category.objects.all()
        context['info_title'] = f'Post > Ordenar por > {order} '
        return context

