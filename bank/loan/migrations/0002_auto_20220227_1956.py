# Generated by Django 3.2.8 on 2022-02-27 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loan', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='status',
            field=models.CharField(choices=[('AV', 'Approved'), ('PD', 'Pending'), ('RJ', 'Rejected')], max_length=2),
        ),
        migrations.AlterField(
            model_name='loanfund',
            name='type',
            field=models.CharField(choices=[('LN', 'Loan'), ('FD', 'Loan Fund')], max_length=2),
        ),
        migrations.AlterField(
            model_name='user',
            name='type',
            field=models.CharField(choices=[('PR', 'Loan Provider'), ('CU', 'Loan Customer'), ('BK', 'Junior')], max_length=2),
        ),
    ]
