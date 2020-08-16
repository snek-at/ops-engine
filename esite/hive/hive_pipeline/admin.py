from wagtail.contrib.modeladmin.options import (
    ModelAdmin,
    ModelAdminGroup,
    modeladmin_register,
)


# Register your registration related models here.

from .models import Pipeline


class PipelineAdmin(ModelAdmin):
    model = Pipeline
    menu_label = "Pipelines"
    menu_icon = "fa-forward"
    menu_order = 290
    add_to_settings_menu = False
    exclude_from_explorer = False

    # Listed in the registration overview
    # list_filter = ("pipeline_activity",)
    # list_display = ('is_active', 'event_name', 'event_scope', 'event_from', 'event_to', 'event_attendees')
    # search_fields = ('is_active', 'event_name', 'event_scope', 'event_from', 'event_to', 'event_attendees')


# modeladmin_register(UserAdmin)


modeladmin_register(PipelineAdmin)

# SPDX-License-Identifier: (EUPL-1.2)
# Copyright © 2020 Simon Prast
