import wagtail.admin.rich_text.editors.draftail.features as draftail_features
from wagtail.admin.rich_text.converters.html_to_contentstate import (
    InlineStyleElementHandler,
)
from wagtail.core import hooks
from .views import ConnectorChooserViewSet


@hooks.register("register_admin_viewset")
def register_connector_chooser_viewset():
    return ConnectorChooserViewSet("connector_chooser", url_prefix="connector-chooser")


# SPDX-License-Identifier: (EUPL-1.2)
# Copyright © 2019-2020 Simon Prast
