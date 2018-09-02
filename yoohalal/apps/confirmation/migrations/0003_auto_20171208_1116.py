# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-08 04:16
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('confirmation', '0002_auto_20171207_1726'),
    ]

    operations = [
        migrations.AlterField(
            model_name='confirmationpayment',
            name='proof_payment',
            field=models.FileField(null=True, upload_to='images/confirmations/', validators=[django.core.validators.FileExtensionValidator(['pdf', 'doc', 'docx', 'jpg', 'jpeg', 'png'])], verbose_name='Proof Of Payment'),
        ),
    ]