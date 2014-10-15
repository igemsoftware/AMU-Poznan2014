"""
.. module:: shweb.designer
   :platform: Unix, Windows
   :synopsis: Module with django views for designer application.

"""
from django.views import generic
from django.shortcuts import redirect

from django.http import Http404, HttpResponse
from django.utils import timezone
from designer.models import DesignProcessModel, STIMULATORS_CHOICE
from designer.forms import DesignProcessForm, DesignProcessSirnaForm
from designer.utils import ShmirDesigner as shmir


class DesignProcessNotifyView(generic.View):
    """View on which API notifies website about finished task by GET request
    (with test_id in url)
    """

    def get(self, request, *args, **kwargs):
        """Method for handling Http GET request. It sets current time timezone
        datetime_finish attribire of DesignProcessModel object (look up by task_id)
        task_id and process_id are used interchangeably

        Args:
            request: django http request object

        Returns:
            django HttpResponse with content_type set to application/json and value "ok"

        Raises:
            Http404
        """
        process_id = kwargs.get('process_id')
        try:
            process = DesignProcessModel.objects.get(process_id=process_id)
        except DesignProcessModel.DoesNotExist:
            raise Http404()

        process.datetime_finish = timezone.now()
        process.save()
        return HttpResponse("ok", content_type='application/json')


class DesignProcessHistoryView(generic.ListView):
    """List view which shows designing process history
    """
    template_name = 'designer/history.html'
    model = DesignProcessModel
    paginate_by = 30

    def get_queryset(self):
        """Overides generic.ListView.get_queryset method to return
        designing history of logged in ordered by datetime_start

        Returns:
            Queryset object (might be empty)
        """
        return self.model.objects.filter(
            user=self.request.user).order_by('-datetime_start')


class DesignProcessDetailView(generic.DetailView):
    """Detail view for single design process. It contains all input, process_id
    and results (if any).
    """
    template_name = 'designer/detail.html'
    model = DesignProcessModel

    def get_object(self, queryset=None):
        """Overides generic.DetailView.get_object to set process_id as a
        lookup field in website's database

        Returns:
            signle DesignProcessModel object
        """
        process_id = self.kwargs.get('process_id')
        try:
            process = DesignProcessModel.objects.get(process_id=process_id)
        except DesignProcessModel.DoesNotExist:
            raise Http404()

        if process.datetime_finish:
            results = shmir.from_transcript_result(process.process_id)
            process.results = results

        if process.stymulators:
            process.stymulators = dict(STIMULATORS_CHOICE)[process.stymulators]
        return process


class DesignProcessSirnaCreateView(generic.CreateView):
    """Create view for DesignProcessModel which is contructed from one or two
    siRNA strands
    """
    template_name = "designer/create.html"
    form_class = DesignProcessSirnaForm
    form_template = "designer/from_sirna.html"
    model = DesignProcessModel

    def get_initial(self):
        """Pre-sets 'email_notify' field in a template to user's email (if logged in)

        Returns:
            None or python dict {'email_notify': USER_EMAIL}
        """
        if self.request.user.is_authenticated():
            return {'email_notify': self.request.user.email}

    def get_context_data(self, **kwargs):
        """Extends generic.CreateView.get_context_data to set additional variable
        'form_template' which is accesible in templates.

        Returns:
            python dict with context to render for template
        """
        context = super(DesignProcessSirnaCreateView, self).get_context_data(**kwargs)
        context['form_template'] = self.form_template
        return context

    def form_valid(self, form):
        """Triggers when form is validated. Sets DesignProcessModel user to currently
        logged in user (otherwise it leaves the field blank)

        Args:
            form: valid DesignProcessModel create form object

        Returns:
            django http redirect object to detailed view of just created DesignProcessModel object
        """
        if self.request.user.id:
            form.instance.user = self.request.user

        form.instance.process_id = shmir.from_sirna_create(form.cleaned_data)
        obj = form.save()
        return redirect('designer:detail', process_id=obj.process_id)


class DesignProcessCreateView(DesignProcessSirnaCreateView):
    """Create view for DesignProcessModel which is contructed from all input values such as:
    transcript', 'min_gc', 'max_gc', 'max_offtarget', 'mirna_name', 'stymulators'.
    Inherited from DesignProcessSirnaCreateView
    """
    template_name = "designer/create.html"
    form_class = DesignProcessForm
    form_template = "designer/form.html"
    model = DesignProcessModel

    def get_context_data(self, **kwargs):
        """Extends DesignProcessSirnaCreateView.get_context_data to set additional variable
        'mirna_name' which is accesible in templates

        Returns:
            python dict with context to render for template
        """
        context = super(DesignProcessCreateView, self).get_context_data(**kwargs)
        context['mirna_name'] = shmir.structures()
        return context

    def form_valid(self, form):
        """Triggers when form is validated. Sets DesignProcessModel user to currently
        logged in user (otherwise it leaves the field blank)

        Args:
            form: valid DesignProcessModel create form object

        Returns:
            django http redirect object to detailed view of just created DesignProcessModel object
        """
        if self.request.user.id:
            form.instance.user = self.request.user

        form.instance.process_id = shmir.from_transcript_create(form.cleaned_data)
        obj = form.save()
        return redirect('designer:detail', process_id=obj.process_id)
