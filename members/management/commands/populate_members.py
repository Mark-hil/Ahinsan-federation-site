from django.core.management.base import BaseCommand
from members.models import Member, Room
import random
from datetime import date, timedelta

class Command(BaseCommand):
    help = 'Populate the database with 100 test members'

    def handle(self, *args, **options):
        first_names = ['John', 'Jane', 'Michael', 'Emily', 'David', 'Sarah', 'Robert', 'Lisa', 
                      'William', 'Jennifer', 'James', 'Elizabeth', 'Joseph', 'Maria', 'Thomas']
        
        last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis',
                     'Rodriguez', 'Martinez', 'Hernandez', 'Lopez', 'Gonzalez', 'Wilson', 'Anderson']
        
        professions = ['Teacher', 'Engineer', 'Doctor', 'Lawyer', 'Business Owner', 
                     'Artist', 'Scientist', 'Mathematician', 'Historian', 'Psychologist']
        
        # Create rooms if they don't exist
        if not Room.objects.exists():
            self.stdout.write("Creating rooms...")
            constellations = ['Andromeda', 'Aquarius', 'Aries', 'Cancer', 'Capricorn', 'Gemini', 
                            'Leo', 'Libra', 'Pisces', 'Sagittarius', 'Scorpio', 'Taurus', 'Virgo']
            
            for constellation in constellations:
                Room.objects.create(name=constellation, capacity=40)
        
        self.stdout.write("Creating test members...")
        
        for i in range(1, 101):
            first_name = random.choice(first_names)
            last_name = random.choice(last_names)
            email = f"{first_name.lower()}.{last_name.lower()}{i}@example.com"
            
            # Generate a random date of birth between 18 and 80 years ago
            start_date = date.today() - timedelta(days=80*365)
            end_date = date.today() - timedelta(days=18*365)
            random_days = random.randint(0, (end_date - start_date).days)
            dob = start_date + timedelta(days=random_days)
            
            member = Member.objects.create(
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone_number=f"233{random.randint(200000000, 299999999)}",
                address=f"{random.randint(1, 1000)} Test St, City {random.randint(1, 10)}",
                guardian_name=f"Guardian {last_name}",
                guardian_phone_number=f"233{random.randint(200000000, 299999999)}",
                date_of_birth=dob,
                gender=random.choice(['male', 'female']),
                profession=random.choice(professions),
                allergies=random.choice(['', 'Peanuts', 'Dust', 'Pollen', '']),
                nhis_number=f"NHIS{random.randint(1000000000, 9999999999)}" if random.random() > 0.3 else '',
                church=random.choice(['', 'First Baptist', 'St. Mary', 'Grace Community', '']),
                district=random.choice(['', 'Accra', 'Kumasi', 'Tamale', 'Cape Coast', ''])
            )
            
            # The save() method will handle room assignment automatically
            
            if i % 10 == 0:
                self.stdout.write(f"Created {i} members...")
        
        self.stdout.write(self.style.SUCCESS(f'Successfully created 100 test members'))
