import firebase_admin
from firebase_admin import credentials, db
import asyncio
import aiohttp
from django.views import View
from django.http import JsonResponse
from asgiref.sync import async_to_sync

cred = credentials.Certificate('utilities/cred.json')

# Check if the default app is already initialized
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://concurrent-demo-default-rtdb.firebaseio.com/'  # Replace with your Firebase Realtime Database URL
    })

class MyView(View):
    async def perform_api_call(self, url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                return await response.json()

    async def save_response_to_firebase(self, response):
        # Add the response to Firebase Realtime Database
        ref = db.reference('api_responses')  # Reference to the 'api_responses' node in the database
        new_response_ref = ref.push()  # Generate a new unique key for the response
        new_response_ref.set(response)  # Set the response data using the unique key

    async def make_api_calls(self, urls):
        for url in urls:
            response = await self.perform_api_call(url)
            await self.save_response_to_firebase(response)

    @async_to_sync
    async def get(self, request):
        urls = [
            'https://jsonplaceholder.typicode.com/posts',
            'https://api.openbrewerydb.org/v1/breweries',
            'https://rickandmortyapi.com/api/character/1,183',
            'https://digimon-api.vercel.app/api/digimon',
            'https://digimoncard.io/api-public/getAllCards.php',
            'https://cataas.com/api/cats?tags=cute',
            'https://api.coinlore.net/api/tickers/',
            'https://api.coinstats.app/public/v1/coins?skip=0&limit=5&currency=EUR',
            'https://www.boredapi.com/api/activity/',
            'https://api.covid19tracker.ca/summary'
            # Add more URLs here
        ]

        await self.make_api_calls(urls)

        return JsonResponse({'message': 'API responses saved to Firebase'})
