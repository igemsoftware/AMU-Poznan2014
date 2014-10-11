from django import forms

from designer.models import DesignProcessModel


class DesignProcessForm(forms.ModelForm):

    class Meta:
        model = DesignProcessModel
        fields = (
            'transcript',
            'min_gc',
            'max_gc',
            'max_off_target',
            'scaffold',
            'stimulators',
        )
