# Generated manually for SubscriptionRequest model

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0013_delete_carlistingpayment'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubscriptionRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('company_name', models.CharField(max_length=255)),
                ('contact_person', models.CharField(max_length=255)),
                ('email', models.EmailField()),
                ('phone', models.CharField(max_length=20)),
                ('subscription_type', models.CharField(max_length=20)),
                ('message', models.TextField(blank=True)),
                ('status', models.CharField(max_length=20, default='pending')),
                ('admin_notes', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]
