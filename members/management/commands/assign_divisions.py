from django.core.management.base import BaseCommand
from members.models import Member
from django.db import transaction

class Command(BaseCommand):
    help = 'Assign divisions to all members who don\'t have one'

    def handle(self, *args, **options):
        # Get all members without a division
        members = Member.objects.filter(division__isnull=True)
        total = members.count()
        
        self.stdout.write(f'Found {total} members without a division')
        
        if total == 0:
            self.stdout.write(self.style.SUCCESS('All members already have divisions assigned'))
            return
            
        # Process in batches to avoid memory issues
        batch_size = 100
        updated = 0
        
        for i in range(0, total, batch_size):
            batch = members[i:i + batch_size]
            with transaction.atomic():
                for member in batch:
                    member.assign_division(save=True)
            
            updated += len(batch)
            self.stdout.write(f'Processed {updated}/{total} members...')
        
        self.stdout.write(self.style.SUCCESS(f'Successfully assigned divisions to {updated} members'))
        
        # Print division counts
        from django.db.models import Count
        division_counts = Member.objects.values('division').annotate(
            count=Count('id')
        ).order_by('division')
        
        self.stdout.write('\nDivision Counts:')
        for div in division_counts:
            self.stdout.write(f"Division {div['division']}: {div['count']} members")
