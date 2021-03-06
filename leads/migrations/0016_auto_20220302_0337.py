# Generated by Django 3.1.4 on 2022-03-02 03:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0015_auto_20220301_1136'),
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='leads.userprofile')),
            ],
        ),
        migrations.AddField(
            model_name='agent',
            name='department',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='agent', to='leads.department'),
        ),
    ]
