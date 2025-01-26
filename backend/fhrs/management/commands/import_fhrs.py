# This is the library that we will use to make HTTP requests to the API
import requests
import xml.etree.ElementTree as ET  # This is the XML parser that we will use to parse the data from the API
from django.core.management.base import BaseCommand  # Import the BaseCommand class from Django
from fhrs.models import Business  # Import the Business model that we created earlier

class Command(BaseCommand):
    help = "Import food hygiene ratings from FHRS API"

    def handle(self, *args, **kwargs):
        url = "https://ratings.food.gov.uk/api/open-data-files/FHRS807en-GB.xml"
        response = requests.get(url)
        
        if response.status_code != 200:
            self.stderr.write("Failed to fetch data")
            return
        
        root = ET.fromstring(response.content)

        # Iterate over each business
        for establishment in root.findall(".//EstablishmentDetail"):
            name = establishment.find("BusinessName").text
            business_type = establishment.find("BusinessType").text
            address_parts = [
                establishment.find(tag).text
                for tag in ["AddressLine1", "AddressLine2", "AddressLine3", "PostCode"]
                if establishment.find(tag) is not None
            ]
            address = ", ".join(address_parts)
            rating = establishment.find("RatingValue").text if establishment.find("RatingValue") is not None else "Not Rated"
            fhrs_id = int(establishment.find("FHRSID").text)
            latitude = float(establishment.find("Geocode/Latitude").text) if establishment.find("Geocode/Latitude") is not None else None
            longitude = float(establishment.find("Geocode/Longitude").text) if establishment.find("Geocode/Longitude") is not None else None

            # Filter only coffee shops or cafés
            if "cafe" in business_type.lower() or "coffee" in business_type.lower():
                obj, created = Business.objects.update_or_create(
                    fhrs_id=fhrs_id,
                    defaults={
                        "name": name,
                        "business_type": business_type,
                        "address": address,
                        "rating": rating,
                        "latitude": latitude,
                        "longitude": longitude
                    },
                )
                self.stdout.write(f"{'Created' if created else 'Updated'}: {name} - {rating}")

        self.stdout.write("Import completed.")
