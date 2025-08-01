# Generated by Django 5.1.7 on 2025-07-31 06:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_content', '0003_alter_coopon_number'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coopon_icool',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=100, null=True)),
                ('number', models.CharField(default=0, max_length=300, unique=True)),
                ('activate', models.BooleanField(default=False)),
                ('edittime', models.DateTimeField(auto_now=True)),
                ('usetime', models.DateTimeField()),
            ],
        ),
    ]
