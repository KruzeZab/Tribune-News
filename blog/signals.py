from django.db.models.signals import pre_save
from django.dispatch import receiver

from .models import Blog

# Define the signal handler function
@receiver(pre_save, sender=Blog)
def check_fake_news(sender, instance, **kwargs):
    # Replace 'API_URL' with the actual URL of your API
    api_url = 'http://127.0.0.1:8000/predict'



    try:

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the JSON response (assuming the API returns JSON)
            api_data = response.json()

            # Update the fields of the 'Blog' instance with data from the API
            instance.title = api_data.get('title', instance.title)
            instance.description = api_data.get('description', instance.description)
            instance.content = api_data.get('content', instance.content)

    except requests.exceptions.RequestException as e:
        # Handle exceptions here (e.g., log the error)
        pass