# Generated by Django 2.2 on 2020-02-24 22:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0005_remove_group_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='slug',
            field=models.CharField(default='', max_length=100, unique=True),
        ),
        migrations.AddField(
            model_name='post',
            name='group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='group_id', to='posts.Group'),
        ),
    ]
