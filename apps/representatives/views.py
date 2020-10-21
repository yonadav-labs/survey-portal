from django.shortcuts import render


def list(request):
    return render(request, 'representatives/table.html', locals())
