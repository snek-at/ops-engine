from wagtail.contrib.modeladmin.options import (
    ModelAdmin,
    ModelAdminGroup,
    modeladmin_register,
)


# Register your registration related models here.

from .models import ContributionFeed, Contributor


class ContribAdmin(ModelAdmin):
    model = ContributionFeed
    menu_label = "Contributions"
    menu_icon = "fa-exclamation-triangle"
    menu_order = 290
    add_to_settings_menu = False
    exclude_from_explorer = False
    
class ContributorAdmin(ModelAdmin):
    model = Contributor
    menu_label = "Contributor"
    menu_icon = "fa-exclamation-triangle"
    menu_order = 290
    add_to_settings_menu = False
    exclude_from_explorer = False

    # Listed in the registration overview
    # list_filter = ("pipeline_activity",)
    # list_display = ('is_active', 'event_name', 'event_scope', 'event_from', 'event_to', 'event_attendees')
    # search_fields = ('is_active', 'event_name', 'event_scope', 'event_from', 'event_to', 'event_attendees')


modeladmin_register(ContributorAdmin)


modeladmin_register(ContribAdmin)

# SPDX-License-Identifier: (EUPL-1.2)
# Copyright © 2019-2020 Simon Prast
