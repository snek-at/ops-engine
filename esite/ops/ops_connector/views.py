from django import forms
from django.contrib.auth import validators
from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _

from generic_chooser.views import ModelChooserViewSet
from django.contrib.auth import get_user_model

from wagtail.admin import widgets
from .models import Connector


class ConnectorForm(forms.ModelForm):
    class Meta:
        model = Connector
        fields = [
            "name",
            "domain",
            "enterprise_page",
        ]


class ConnectorChooserViewSet(ModelChooserViewSet):
    icon = "pilcrow"
    model = Connector
    page_title = _("Choose a connector")
    per_page = 10
    form_class = ConnectorForm


# Create your views here.

# SPDX-License-Identifier: (EUPL-1.2)
# Copyright © 2019-2020 Simon Prast
