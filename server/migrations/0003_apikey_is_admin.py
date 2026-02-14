# Generated manually for adding is_admin field to ApiKey model

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0002_apikey_notification_source'),
    ]

    operations = [
        migrations.AddField(
            model_name='apikey',
            name='is_admin',
            field=models.BooleanField(default=False, help_text='Permisos de administrador'),
        ),
    ]