# Generated by Django 2.0.3 on 2018-04-02 14:38
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):
    dependencies = [("tokenauth", "0001_initial")]

    operations = [
        migrations.AddField(
            model_name="authtoken",
            name="next_url",
            field=models.CharField(blank=True, max_length=2000),
        )
    ]
