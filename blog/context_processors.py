from .forms import SearchForm
from .models import Board

def search_form(request):
    search_form = SearchForm()
    return {"search_form": search_form}

def top_boards(request):
    return {'popular_boards': sorted(Board.objects.all(), key=lambda obj: -obj.get_popularity_rating())[:4]}