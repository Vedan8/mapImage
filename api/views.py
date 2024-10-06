import math
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class MapImagesView(APIView):

    def post(self, request):
        """
        Handle POST requests to fetch 9 satellite images for the given latitude and longitude.
        """
        latitude = request.data.get('latitude')
        longitude = request.data.get('longitude')

        if latitude is None or longitude is None:
            return Response({"error": "Latitude and Longitude are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            latitude = float(latitude)
            longitude = float(longitude)
        except ValueError:
            return Response({"error": "Invalid latitude or longitude."}, status=status.HTTP_400_BAD_REQUEST)

        image_urls = self.get_nearby_image_urls(latitude, longitude)

        return Response({"images": image_urls}, status=status.HTTP_200_OK)

    def get_nearby_image_urls(self, latitude, longitude):
        """
        Generate 9 nearby satellite image URLs.
        """
        image_urls = []
        
        # Define offsets for creating a 3x3 grid of images
        offsets = [-1, 0, 1]  # offsets for x and y
        zoom = 19  # Zoom level (higher number for more detail)

        for dx in offsets:
            for dy in offsets:
                # Calculate the tile coordinates
                x, y = self.lat_lon_to_tile(latitude, longitude, zoom)
                x += dx
                y += dy
                
                # Use OpenStreetMap tile server for satellite imagery
                image_url = f"https://a.tile.openstreetmap.org/{zoom}/{x}/{y}.png"
                image_urls.append(image_url)

        return image_urls

    def lat_lon_to_tile(self, lat, lon, zoom):
        """
        Convert latitude and longitude to tile numbers.
        """
        lat_rad = math.radians(lat)
        n = 2.0 ** zoom
        x = int((lon + 180.0) / 360.0 * n)
        y = int((1.0 - (math.log(math.tan(lat_rad) + (1 / math.cos(lat_rad))) / math.pi)) / 2.0 * n)

        return x, y
