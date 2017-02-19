from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .forms import BrewForm, BeerForm, UserForm
from .models import Brewery, Beer

IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']


def create_brew(request):
    if not request.user.is_authenticated():
        return render(request, 'texasbrew/login.html')
    else:
        form = BrewForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            brew = form.save(commit=False)
            brew.user = request.user
            brew.brew_logo = request.FILES['brew_logo']
            file_type = brew.brew_logo.url.split('.')[-1]
            file_type = file_type.lower()
            if file_type not in IMAGE_FILE_TYPES:
                context = {
                    'brewery': brew,
                    'form': form,
                    'error_message': 'Image file must be PNG, JPG, or JPEG',
                }
                return render(request, 'texasbrew/create_album.html', context)
            brew.save()
            return render(request, 'texasbrew/detail.html', {'brewery': brew})
        context = {
            "form": form,
        }
        return render(request, 'texasbrew/create_album.html', context)


def create_beer(request, brewery_id):
    form = BeerForm(request.POST or None, request.FILES or None)
    brewery = get_object_or_404(Brewery, pk=brewery_id)
    if form.is_valid():
        brewery_beers = brewery.beer_set.all()
        for s in brewery_beers:
            if s.beer_name == form.cleaned_data.get("beer_name"):
                context = {
                    'brewery': brewery,
                    'form': form,
                    'error_message': 'You already added that beer',
                }
                return render(request, 'texasbrew/create_song.html', context)
        beer = form.save(commit=False)
        beer.brewery = brewery
        beer.image = request.FILES['beer_image']
        file_type = beer.beer_image.url.split('.')[-1]
        file_type = file_type.lower()
        if file_type not in IMAGE_FILE_TYPES:
            context = {
                'brewery': brewery,
                'form': form,
                'error_message': 'Image file must be png, jpg, jpeg',
            }
            return render(request, 'texasbrew/create_song.html', context)

        beer.save()
        return render(request, 'texasbrew/detail.html', {'brewery': brewery})
    context = {
        'brewery': brewery,
        'form': form,
    }
    return render(request, 'texasbrew/create_song.html', context)


def delete_brewery(request, brewery_id):
    brewery = Brewery.objects.get(pk=brewery_id)
    brewery.delete()
    brewery = Brewery.objects.filter(user=request.user)
    return render(request, 'texasbrew/index.html', {'brewery': brewery})


def delete_beer(request, brewery_id, beer_id):
    brewery = get_object_or_404(Brewery, pk=brewery_id)
    beer = Beer.objects.get(pk=beer_id)
    beer.delete()
    return render(request, 'texasbrew/detail.html', {'brewery': brewery})


def detail(request, brewery_id):
    if not request.user.is_authenticated():
        return render(request, 'texasbrew/login.html')
    else:
        user = request.user
        brewery = get_object_or_404(Brewery, pk=brewery_id)
        return render(request, 'texasbrew/detail.html', {'brewery': brewery, 'user': user})


def favorite(request, beer_id):
    beer = get_object_or_404(Beer, pk=beer_id)
    try:
        if beer.is_favorite:
            beer.is_favorite = False
        else:
            beer.is_favorite = True
        beer.save()
    except (KeyError, Beer.DoesNotExist):
        return JsonResponse({'success': False})
    else:
        return JsonResponse({'success': True})


def favorite_brewery(request, brewery_id):
    brewery = get_object_or_404(Brewery, pk=brewery_id)
    try:
        if brewery.is_favorite:
            brewery.is_favorite = False
        else:
            brewery.is_favorite = True
        brewery.save()
    except (KeyError, Brewery.DoesNotExist):
        return JsonResponse({'success': False})
    else:
        return JsonResponse({'success': True})


def index(request):
    if not request.user.is_authenticated():
        return render(request, 'texasbrew/login.html')
    else:
        breweries = Brewery.objects.filter(user=request.user)
        beer_results = Beer.objects.all()
        query = request.GET.get("q")
        if query:
            breweries = breweries.filter(
                Q(brew_name__icontains=query)
            ).distinct()
            beer_results = beer_results.filter(
                Q(beer_name__icontains=query)
            ).distinct()
            return render(request, 'texasbrew/index.html', {
                'breweries': breweries,
                'beers': beer_results,
            })
        else:
            return render(request, 'texasbrew/index.html', {'breweries': breweries})


def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'texasbrew/login.html', context)


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                breweries = Brewery.objects.filter(user=request.user)
                return render(request, 'texasbrew/index.html', {'breweries': breweries})
            else:
                return render(request, 'texasbrew/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'texasbrew/login.html', {'error_message': 'Invalid login'})
    return render(request, 'texasbrew/login.html')


def register(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                breweries = Brewery.objects.filter(user=request.user)
                return render(request, 'texasbrew/index.html', {'breweries': breweries})
    context = {
        "form": form,
    }
    return render(request, 'texasbrew/register.html', context)


def beers(request, filter_by):
    if not request.user.is_authenticated():
        return render(request, 'texasbrew/login.html')
    else:
        try:
            beer_ids = []
            for brewery in Brewery.objects.filter(user=request.user):
                for beer in brewery.beer_set.all():
                    beer_ids.append(beer.pk)
            users_beers = Beer.objects.filter(pk__in=beer_ids)
            if filter_by == 'favorites':
                users_beers = users_beers.filter(is_favorite=True)
        except Brewery.DoesNotExist:
            users_beers = []
        return render(request, 'texasbrew/songs.html', {
            'beer_list': users_beers,
            'filter_by': filter_by,
        })
