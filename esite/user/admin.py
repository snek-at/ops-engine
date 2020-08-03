from wagtail.contrib.modeladmin.options import (
    ModelAdmin,
    ModelAdminGroup,
    modeladmin_register,
)

from .models import User

# Register your user related models here.


class UserAdmin(ModelAdmin):
    model = User
    menu_label = "User"
    menu_icon = "user"
    menu_order = 290
    add_to_settings_menu = False
    exclude_from_explorer = False

    # Listed in the user overview
    list_display = ("date_joined", "username", "email")
    search_fields = ("date_joined", "username", "email")


class CustomerAdminB(ModelAdminGroup):
    menu_label = "User Management"
    menu_icon = "group"
    menu_order = 110
    add_to_settings_menu = False
    exclude_from_explorer = False
    items = (UserAdmin,)


# SPDX-License-Identifier: (EUPL-1.2)
# Copyright © 2019-2020 Simon Prast
