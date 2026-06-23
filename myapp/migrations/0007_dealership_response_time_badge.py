from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0006_car_exterior_color_car_interior_color_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='dealership',
            name='response_time_badge_enabled',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='dealership',
            name='response_time_badge_choice',
            field=models.CharField(choices=[('10_min', '10 min'), ('1_hr', '1 hr'), ('3_hr', '3 hr'), ('6_hr', '6 hr'), ('24_hr', '24 hr')], default='', max_length=20, blank=True),
        ),
    ]
