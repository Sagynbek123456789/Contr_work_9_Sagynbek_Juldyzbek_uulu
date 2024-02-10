from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import CreateView, UpdateView, DeleteView
from webapp.models import Review, Project
from django.urls import reverse
from django.shortcuts import get_object_or_404, redirect
from webapp.forms import ReviewForm


class ReviewCreateView(LoginRequiredMixin, CreateView):
    template_name = 'reviews/review_create.html'
    model = Review
    form_class = ReviewForm

    def form_valid(self, form):
        project = get_object_or_404(Project, pk=self.kwargs.get('pk'))
        review = form.save(commit=False)
        review.project = project
        review.author = self.request.user
        review.save()
        return redirect('webapp:project_view', pk=project.pk)


class ReviewUpdateView(PermissionRequiredMixin, UpdateView):
    template_name = 'reviews/review_update.html'
    model = Review
    form_class = ReviewForm
    permission_required = 'webapp.change_review'

    def has_permission(self):
        return super().has_permission() or self.request.user == self.get_object().author

    def get_success_url(self):
        return reverse('webapp:project_view', kwargs={'pk': self.object.project.pk})


class ReviewDeleteView(PermissionRequiredMixin, DeleteView):
    model = Review
    permission_required = 'webapp.delete_review'

    def has_permission(self):
        return super().has_permission() or self.request.user == self.get_object().author

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('webapp:project_view', kwargs={'pk': self.object.project.pk})

