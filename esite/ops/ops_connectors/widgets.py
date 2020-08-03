from django.contrib.admin.utils import quote
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from generic_chooser.widgets import AdminChooser


class ConnectorChooser(AdminChooser):
    from .models import Connector

    choose_one_text = _("Choose a connector")
    link_to_chosen_text = _("Edit this connector")
    model = Connector
    choose_modal_url_name = "connector_chooser:choose"

    def get_edit_item_url(self, item):
        return reverse(
            "wagtailsnippets:edit", args=("base", "connector", quote(item.pk))
        )


# SPDX-License-Identifier: (EUPL-1.2)
# Copyright © 2019-2020 Simon Prast
