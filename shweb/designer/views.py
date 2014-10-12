from django.views import generic
from django.shortcuts import redirect

from django.http import Http404
from designer.models import DesignProcessModel
from designer.forms import DesignProcessForm
from designer.utils import shmir_post_task


class DesignProcessHistoryView(generic.ListView):
    template_name = 'designer/history.html'
    model = DesignProcessModel
    paginate_by = 30

    def get_queryset(self):
        return self.model.objects.filter(
            user=self.request.user).order_by('-datetime_start')

    # def get_context_data(self, *args, **kwargs):
    #     con = super(DesignProcessHistoryView, self).get_context_data()
    #     import ipdb; ipdb.set_trace()  # HARDCODED


class DesignProcessDetailView(generic.DetailView):
    template_name = 'designer/detail.html'
    model = DesignProcessModel

    def get_object(self, queryset=None):
        process_id = self.kwargs.get('process_id')
        try:
            process = DesignProcessModel.objects.get(process_id=process_id)
        except DesignProcessModel.DoesNotExist:
            raise Http404()

        return process


class DesignProcessCreateView(generic.CreateView):
    template_name = "designer/create.html"
    form_class = DesignProcessForm
    model = DesignProcessModel

    def get_context_data(self, **kwargs):
        context = super(DesignProcessCreateView, self).get_context_data(**kwargs)
        context['scaffold'] = (
            'all',
            'miR-30a',
            'miR-155',
            'miR-21',
            'miR-122',
            'miR-31',
        )
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.process_id = shmir_post_task()
        obj = form.save()
        return redirect('designer:detail', process_id=obj.process_id)
