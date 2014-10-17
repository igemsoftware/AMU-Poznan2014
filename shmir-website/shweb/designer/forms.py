"""
.. module:: shweb.designer
   :platform: Unix, Windows
   :synopsis: Module with forms for designing process
"""
from django import forms

from designer.models import DesignProcessModel

TRANSCRIPT_FIELDS = (
    'transcript',
    'min_gc',
    'max_gc',
    'max_offtarget',
    'mirna_name',
    'stymulators',
    'email_notify'
)

SIRNA_FIELDS = (
    'sirna',
    'email_notify'
)


class DesignProcessForm(forms.ModelForm):
    """Form for designing process from structure
    """

    def __init__(self, *args, **kwargs):
        """__init__ function for designing process. It sets all fields as
        required except for email_notify field.
        """
        super(DesignProcessForm, self).__init__(*args, **kwargs)

        for key in self.fields:
            self.fields[key].required = True

        self.fields['email_notify'].required = False

    class Meta:
        model = DesignProcessModel
        fields = TRANSCRIPT_FIELDS


class DesignProcessSirnaForm(forms.ModelForm):
    """Form for designing process from siRNA strands
    """

    def __init__(self, *args, **kwargs):
        """__init__ function for designing process. It sets all fields as
        required except for email_notify field.
        """
        super(DesignProcessSirnaForm, self).__init__(*args, **kwargs)

        for key in self.fields:
            self.fields[key].required = True

        self.fields['email_notify'].required = False

    class Meta:
        model = DesignProcessModel
        fields = SIRNA_FIELDS
