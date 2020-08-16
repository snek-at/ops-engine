from wagtail.contrib.modeladmin.options import (
    ModelAdmin,
    ModelAdminGroup,
    modeladmin_register,
)


# Register your registration related models here.

from .models import Gitlab


class GitlabAdmin(ModelAdmin):
    model = Gitlab
    menu_label = "Gitlabs"
    menu_icon = "fa-gitlab"
    menu_order = 290
    add_to_settings_menu = False
    exclude_from_explorer = False

    # Listed in the registration overview
    # list_filter = ('is_active','event_name')
    # list_display = ('is_active', 'event_name', 'event_scope', 'event_from', 'event_to', 'event_attendees')
    # search_fields = ('is_active', 'event_name', 'event_scope', 'event_from', 'event_to', 'event_attendees')


# modeladmin_register(UserAdmin)


modeladmin_register(GitlabAdmin)

# SPDX-License-Identifier: (EUPL-1.2)
# Copyright © 2020 Simon Prast
