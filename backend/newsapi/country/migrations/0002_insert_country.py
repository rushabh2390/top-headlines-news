from django.db import migrations, models

def insert_data(apps, schema_editor):
    country = apps.get_model('country', 'Country')

    # Create and save instances of YourModel to insert data
    country.objects.create(country_name='America', country_code='us')
    country.objects.create(country_name='India', country_code='in')

class Migration(migrations.Migration):

    dependencies = [
        ('country', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(insert_data),
    ]
