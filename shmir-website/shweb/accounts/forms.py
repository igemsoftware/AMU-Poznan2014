"""
.. module:: shweb.accounts
   :platform: Unix, Windows
   :synopsis: Module with forms for custom accounts

"""
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from accounts.models import UserProfile


class CustomUserCreationForm(UserCreationForm):
    """Form for user creating.
    """

    def __init__(self, *args, **kargs):
        """Custom __init__ method which deletes 'username' field.
        """
        super(CustomUserCreationForm, self).__init__(*args, **kargs)
        del self.fields['username']

    class Meta:
        model = UserProfile
        fields = ("email",)


class CustomUserChangeForm(UserChangeForm):
    """Form for user changing.
    """

    def __init__(self, *args, **kargs):
        """Custom __init__ method which deletes 'username' field.
        """
        super(CustomUserChangeForm, self).__init__(*args, **kargs)
        del self.fields['username']

    class Meta:
        model = UserProfile
