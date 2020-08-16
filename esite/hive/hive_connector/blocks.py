from django.utils.functional import cached_property
from django.utils.html import format_html

from wagtail.core.blocks import ChooserBlock
from wagtail.core.utils import resolve_model_string


class ConnectorChooserBlock(ChooserBlock):
    @cached_property
    def target_model(self):
        from .models import Connector

        return Connector

    @cached_property
    def widget(self):
        from .widgets import ConnectorChooser

        return ConnectorChooser

    def render_basic(self, value, context=None):
        if value:
            return format_html('<a href="{0}">{1}</a>', value.username, value.email)
        else:
            return ""

    class Meta:
        icon = "user"
        name = "user"


# SPDX-License-Identifier: (EUPL-1.2)
# Copyright © 2020 Simon Prast
