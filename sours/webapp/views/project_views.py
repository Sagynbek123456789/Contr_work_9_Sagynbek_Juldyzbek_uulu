from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.utils.http import urlencode

from django.db.models import Q
from webapp.models import Project
from webapp.forms import ProjectForm, SimpleSearchForm
from django.views.generic import View, FormView, ListView, DetailView, CreateView, UpdateView, DeleteView


class IndexView(ListView):
    model = Project
    template_name = 'projects/index.html'
    context_object_name = 'projects'
    paginate_by = 6
    paginate_orphans = 3
    ordering = ('-created',)

    def get_search_form(self):
        return SimpleSearchForm(self.request.GET)

    def get_search_value(self):
        if self.search_form.is_valid():
            return self.search_form.cleaned_data['search']
        return None

    def dispatch(self, request, *args, **kwargs):
        print(request.user)
        self.search_form = self.get_search_form()
        self.search_value = self.get_search_value()
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.search_value:
            queryset = queryset.filter(Q(title__icontains=self.search_value) |
                                       Q(content__icontains=self.search_value))
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['form'] = self.search_form
        if self.search_value:
            context['query'] = urlencode({'search': self.search_value})
            context['search_value'] = self.search_value
        return context


class ProjectView(DetailView):
    model = Project
    template_name = 'projects/project_view.html'
    context_object_name = 'project'  # Указываем имя переменной для передачи объекта проекта в шаблон

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем логику для получения отзывов и передачи их в контекст шаблона
        project = self.get_object()
        context['reviews'] = project.reviews.all()  # Здесь reviews - связь с отзывами проекта
        return context


class ProjectCreateView(LoginRequiredMixin, CreateView):
    template_name = 'projects/project_create.html'
    model = Project
    # fields = ['title', 'content', 'author', 'tags']
    form_class = ProjectForm

    def form_valid(self, form):
        self.project = form.save(commit=False)
        self.project.author = self.request.user
        self.project.save()
        form.save_m2m()
        return redirect('webapp:project_view', pk=self.project.pk)


class ProjectUpdateView(PermissionRequiredMixin, UpdateView):
    template_name = 'projects/project_update.html'
    model = Project
    form_class = ProjectForm
    permission_required = 'webapp.change_project'

    def has_permission(self):
        return super().has_permission() or self.request.user == self.get_object().author

    def get_success_url(self):
        return reverse('webapp:project_view', kwargs={'pk': self.object.pk})


class ProjectDeleteView(UserPassesTestMixin, DeleteView):
    template_name = 'projects/project_delete.html'
    model = Project
    success_url = reverse_lazy('webapp:index')

    def test_func(self):
        project = self.get_object()
        return self.request.user.has_perm('webapp.delete_project') or self.request.user == project.author

    def get_success_url(self):
        return reverse_lazy('webapp:index')
