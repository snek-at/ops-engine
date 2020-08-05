# Generated by Django 2.2.12 on 2020-08-03 00:39

from django.db import migrations
import esite.colorfield.blocks
import wagtail.core.blocks
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('ops_scpages', '0009_auto_20200803_0200'),
    ]

    operations = [
        migrations.AddField(
            model_name='opsscpagespage',
            name='feed',
            field=wagtail.core.fields.StreamField([('feed', wagtail.core.blocks.StructBlock([('datetime', wagtail.core.blocks.DateTimeBlock(null=True, required=True)), ('data', wagtail.core.blocks.StreamBlock([('commit', wagtail.core.blocks.StructBlock([('contribution_id', wagtail.core.blocks.CharBlock()), ('date', wagtail.core.blocks.DateTimeBlock()), ('message', wagtail.core.blocks.TextBlock()), ('files', wagtail.core.blocks.StreamBlock([('file', wagtail.core.blocks.StructBlock([('insertions', wagtail.core.blocks.CharBlock()), ('deletions', wagtail.core.blocks.CharBlock()), ('path', wagtail.core.blocks.CharBlock()), ('raw_changes', wagtail.core.blocks.TextBlock())], blank=True, icon='fa-newspaper-o', null=True))], blank=True, null=True))], blank=True, icon='fa-newspaper-o', null=True)), ('issue', wagtail.core.blocks.StructBlock([('contribution_id', wagtail.core.blocks.CharBlock()), ('date', wagtail.core.blocks.DateTimeBlock()), ('message', wagtail.core.blocks.TextBlock()), ('files', wagtail.core.blocks.StreamBlock([('file', wagtail.core.blocks.StructBlock([('insertions', wagtail.core.blocks.CharBlock()), ('deletions', wagtail.core.blocks.CharBlock()), ('path', wagtail.core.blocks.CharBlock()), ('raw_changes', wagtail.core.blocks.TextBlock())], blank=True, icon='fa-newspaper-o', null=True))], blank=True, null=True))], blank=True, icon='fa-newspaper-o', null=True)), ('pr', wagtail.core.blocks.StructBlock([('contribution_id', wagtail.core.blocks.CharBlock()), ('date', wagtail.core.blocks.DateTimeBlock()), ('message', wagtail.core.blocks.TextBlock()), ('files', wagtail.core.blocks.StreamBlock([('file', wagtail.core.blocks.StructBlock([('insertions', wagtail.core.blocks.CharBlock()), ('deletions', wagtail.core.blocks.CharBlock()), ('path', wagtail.core.blocks.CharBlock()), ('raw_changes', wagtail.core.blocks.TextBlock())], blank=True, icon='fa-newspaper-o', null=True))], blank=True, null=True))], blank=True, icon='fa-newspaper-o', null=True)), ('review', wagtail.core.blocks.StructBlock([('contribution_id', wagtail.core.blocks.CharBlock()), ('date', wagtail.core.blocks.DateTimeBlock()), ('message', wagtail.core.blocks.TextBlock()), ('files', wagtail.core.blocks.StreamBlock([('file', wagtail.core.blocks.StructBlock([('insertions', wagtail.core.blocks.CharBlock()), ('deletions', wagtail.core.blocks.CharBlock()), ('path', wagtail.core.blocks.CharBlock()), ('raw_changes', wagtail.core.blocks.TextBlock())], blank=True, icon='fa-newspaper-o', null=True))], blank=True, null=True))], blank=True, icon='fa-newspaper-o', null=True))], blank=True, null=True))], blank=False, icon='fa-newspaper-o', null=True))], blank=True, null=True),
        ),
        migrations.AddField(
            model_name='opsscpagespage',
            name='statistic',
            field=wagtail.core.fields.StreamField([('statistic', wagtail.core.blocks.StructBlock([('insertions', wagtail.core.blocks.CharBlock()), ('deletions', wagtail.core.blocks.CharBlock()), ('languages', wagtail.core.blocks.StreamBlock([('language', wagtail.core.blocks.StructBlock([('language_name', wagtail.core.blocks.CharBlock()), ('color', esite.colorfield.blocks.ColorBlock()), ('insertions', wagtail.core.blocks.CharBlock()), ('deletions', wagtail.core.blocks.CharBlock())], blank=True, icon='fa-newspaper-o', null=True))], blank=True, null=True))], blank=False, icon='fa-newspaper-o', null=True))], blank=True, null=True),
        ),
    ]