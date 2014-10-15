from django.views import generic
from django.shortcuts import redirect
import uuid

from django.http import Http404
from designer.models import DesignProcessModel, STIMULATORS_CHOICE
from designer.forms import DesignProcessForm
from designer.utils import ShmirDesigner as shmir


class DesignProcessHistoryView(generic.ListView):
    template_name = 'designer/history.html'
    model = DesignProcessModel
    paginate_by = 30

    def get_queryset(self):
        return self.model.objects.filter(
            user=self.request.user).order_by('-datetime_start')


class DesignProcessDetailView(generic.DetailView):
    template_name = 'designer/detail.html'
    model = DesignProcessModel

    def get_object(self, queryset=None):
        process_id = self.kwargs.get('process_id')
        try:
            process = DesignProcessModel.objects.get(process_id=process_id)
        except DesignProcessModel.DoesNotExist:
            raise Http404()

        process.stymulators = dict(STIMULATORS_CHOICE)[process.stymulators]
        return process


class DesignProcessCreateView(generic.CreateView):
    template_name = "designer/create.html"
    form_class = DesignProcessForm
    model = DesignProcessModel

    def get_context_data(self, **kwargs):
        context = super(DesignProcessCreateView, self).get_context_data(**kwargs)
        context['mirna_name'] = shmir.structures()
        return context

    def form_valid(self, form):
        if self.request.user.id:
            form.instance.user = self.request.user

        form.instance.process_id = shmir.from_transcript_create(form.cleaned_data)
        obj = form.save()
        return redirect('designer:detail', process_id=obj.process_id)
