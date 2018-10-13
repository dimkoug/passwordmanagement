# Generated by Django 2.1.2 on 2018-10-13 08:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AccountType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'account type',
                'verbose_name_plural': 'account types',
                'default_related_name': 'accounttypes',
            },
        ),
        migrations.CreateModel(
            name='Password',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('username', models.CharField(max_length=100)),
                ('password', models.CharField(max_length=255)),
                ('comments', models.TextField(blank=True)),
                ('url', models.URLField()),
                ('account_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='passwords', to='projects.AccountType')),
            ],
            options={
                'verbose_name': 'password',
                'verbose_name_plural': 'passwords',
                'default_related_name': 'passwords',
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'project',
                'verbose_name_plural': 'projects',
                'default_related_name': 'projects',
            },
        ),
        migrations.AddField(
            model_name='password',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='passwords', to='projects.Project'),
        ),
    ]
