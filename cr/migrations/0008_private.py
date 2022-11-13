# Generated by Django 3.2.4 on 2021-09-10 04:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cr', '0007_feedback'),
    ]

    operations = [
        migrations.CreateModel(
            name='private',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chat', models.CharField(max_length=9999999)),
                ('pid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cr.profile')),
                ('regid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cr.register')),
            ],
        ),
    ]
