from django.shortcuts import render

# Create your views here.
def show_main(request):
    context = {
        'title': 'Anoooooomgh',
        'language': 'Zimbabwe',
        'firstName': 'Rakha',
        'lastName': 'Abid'
    }

    return render(request, "main.html", context)