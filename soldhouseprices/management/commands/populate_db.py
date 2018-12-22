from soldhouseprices.models import HouseData
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Initialization of postgresql with house_data file.'

    def add_arguments(self, parser):
        parser.add_argument('file location', type=str, nargs='?', default=None, help='Location of the house_data file.')

    def handle(self, *args, **options):
        total_count = HouseData.objects.count()
        file_location = options.get('file location', None)

        if file_location is None:
            self.stdout.write(self.style.ERROR('File location is required for populating database!'))
            self.stdout.write(self.style.WARNING('Usage: python manager.py populate_db file-location'))
            return

        if total_count == 0:
            insert_count = HouseData.copy_objects.from_csv(file_location)
            self.stdout.write(self.style.SUCCESS('%s records inserted!' % insert_count))
        else:
            self.stdout.write(self.style.ERROR('Database already has populated!'))
