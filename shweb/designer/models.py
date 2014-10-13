import re

from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.urlresolvers import reverse

STIMULATORS_CHOICE = (
    ('1', 'yes'),
    ('-1', 'no'),
    ('0', 'no diference'),
)


class DesignProcessModel(models.Model):
    user = models.ForeignKey(get_user_model(), blank=True, null=True)
    process_id = models.CharField(max_length=36)
    transcript = models.CharField(
        'transcript name',
        max_length=20,
        validators=[lambda x: re.search(r"[A-Za-z0-9_.]+", x)],
        help_text='Should content only alphanumeric plus . (dot) _ (underscore) - (dash)'
    )
    min_gc = models.IntegerField(
        "minimum 'GC' content",
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        default=40,
        help_text="You can choose between 0-100 (scroll)",
    )
    max_gc = models.IntegerField(
        "maximum 'GC' content",
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        default=60,
        help_text="You can choose between 0-100 (scroll)",
    )
    max_offtarget = models.IntegerField(
        "maximum of off-target transcripts",
        validators=[MinValueValidator(0), MaxValueValidator(1000)],
        default=10,
        help_text="You can choose between 0-1000 (scroll)"
    )
    stymulators = models.CharField(
        "stimulatory sequences",
        max_length=10,
        choices=STIMULATORS_CHOICE,
        default=None,
    )
    mirna_name = models.CharField("miRNA scaffold", max_length=20)
    datetime_start = models.DateTimeField(auto_now_add=True)
    datetime_finish = models.DateTimeField(blank=True, null=True)

    def __unicode__(self):
        return self.process_id

    def get_absolute_url(self):
        return reverse('designer:detail', kwargs={'process_id': self.process_id})
