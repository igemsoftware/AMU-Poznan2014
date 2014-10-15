"""
.. module:: shweb.designer
   :platform: Unix, Windows
   :synopsis: Module with database design model.
"""

import re

from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.urlresolvers import reverse

STIMULATORS_CHOICE = (
    ('yes', 'yes'),
    ('no', 'no'),
    ('no_diference', 'no diference'),
)


class DesignProcessModel(models.Model):
    """Design process model, which saves all input.
    """
    user = models.ForeignKey(get_user_model(), blank=True, null=True)
    process_id = models.CharField(max_length=36)
    transcript = models.CharField(
        'transcript name',
        max_length=20,
        validators=[lambda x: re.search(r"[A-Za-z0-9_.]+", x)],
        help_text='Should content only alphanumeric plus . (dot) _ (underscore) - (dash)',
        blank=True,
        null=True,
    )
    min_gc = models.IntegerField(
        "minimum 'GC' content",
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        default=40,
        help_text="You can choose between 0-100 (scroll)",
        blank=True,
        null=True,
    )
    max_gc = models.IntegerField(
        "maximum 'GC' content",
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        default=60,
        help_text="You can choose between 0-100 (scroll)",
        blank=True,
        null=True,
    )
    max_offtarget = models.IntegerField(
        "maximum of off-target transcripts",
        validators=[MinValueValidator(0), MaxValueValidator(1000)],
        default=10,
        help_text="You can choose between 0-1000 (scroll)",
        blank=True,
        null=True,
    )
    stymulators = models.CharField(
        "stimulatory sequences",
        max_length=20,
        choices=STIMULATORS_CHOICE,
        default=None,
        blank=True,
        null=True,
    )
    mirna_name = models.CharField(
        "miRNA scaffold",
        blank=True,
        null=True,
        max_length=20
    )
    email_notify = models.EmailField(
        "Your e-mail",
        blank=True,
        null=True,
        help_text="Type your e-mail, if you want to "
                  "be notified about task completion. "
                  "Otherwise leave the field blank."
    )

    sirna = models.CharField(
        "siRNA",
        max_length=60,
        blank=True,
        null=True,
        help_text="Type one or two siRNA strands."
    )
    datetime_start = models.DateTimeField(auto_now_add=True)
    datetime_finish = models.DateTimeField(blank=True, null=True)

    def __unicode__(self):
        """It is responsible for proper model presentation as a variable.

        Returns
            str object
        """
        return self.process_id

    def get_absolute_url(self):
        """It is responsible for generating detail url for design model.self

        Returns:
            str object - url for detailed view
        """
        return reverse('designer:detail', kwargs={'process_id': self.process_id})
