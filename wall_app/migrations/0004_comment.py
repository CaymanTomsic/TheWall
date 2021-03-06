# Generated by Django 2.2.4 on 2020-10-14 22:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wall_app', '0003_postedmessage'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment_text', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('posted_message', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='wall_app.PostedMessage')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='wall_app.User')),
            ],
        ),
    ]
