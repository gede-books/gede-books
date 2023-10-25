from django.shortcuts import render

# Create your views here.
def show_main(request):
    context = {
        'title': 'Aooooooomgh',
        'language': 'English',
        'firstName': 'Rakha',
        'lastName': 'Abid',
    }

    return render(request, "main.html", context)