from .forms import all_categories

def add_categories(request):
    return {
        'categories': all_categories()
    }