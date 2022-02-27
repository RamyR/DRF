# Generated by Django 3.2.8 on 2022-02-27 16:01

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateTimeField()),
                ('status', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='LoanFund',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('duration', models.DurationField()),
                ('min_amount', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('max_amount', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('interest_rate', models.DecimalField(decimal_places=3, max_digits=5)),
                ('type', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('email_address', models.EmailField(max_length=254)),
                ('type', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(2)])),
                ('password', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('date', models.DateTimeField()),
                ('application', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='payments', to='loan.application')),
            ],
        ),
        migrations.AddField(
            model_name='application',
            name='loan_fund',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='applications', to='loan.loanfund'),
        ),
        migrations.AddField(
            model_name='application',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='applications', to='loan.user'),
        ),
    ]
