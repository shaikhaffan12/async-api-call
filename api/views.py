import firebase_admin
from firebase_admin import credentials, db
import asyncio
import aiohttp
from django.views import View
from django.http import JsonResponse
from asgiref.sync import async_to_sync
from django.views.decorators.csrf import csrf_exempt

cred = credentials.Certificate('utilities/cred.json')

# Check if the default app is already initialized
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://concurrent-demo-default-rtdb.firebaseio.com/'  
    })

class MyView(View):
    @csrf_exempt
    async def perform_api_call(self, url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                return await response.json()

    async def make_api_calls(self, urls):
        tasks = []
        for url in urls:
            task = asyncio.create_task(self.perform_api_call(url))
            tasks.append(task)
        return await asyncio.gather(*tasks)

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

        results = await self.make_api_calls(urls)

        data = {
            "data":results
            # Add more fields as needed
        }

        ref = db.reference('data')

        ref.set(data)

        # Retrieve data from Firebase Realtime Database
        # ref = db.reference('data')
        # name = ref.child('name').get()
        # gender = ref.child('gender').get()
        # status = ref.child('status').get()

        # print(name, gender, status)

        return JsonResponse(results, safe=False)


