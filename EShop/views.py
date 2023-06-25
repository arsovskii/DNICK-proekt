import json

from django.contrib.auth import hashers
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.db import models
from django.db.models import Q
from django.http import HttpResponse, FileResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.cache import cache_control
from django.contrib.auth.forms import PasswordChangeForm

from EShop.filters import ProductFilter
from EShop.forms import BuyerForm, ProductForm, ImageFormSet, UserPictureUpdateForm, TagForm
from EShop.models import BuyerUser, DeveloperUser, Product, Tag
from EShop.utils import infoContext

LIMITSEARCH = 11
PAGINATIONSIZE = 10
POPULARITYCUTOFF = 75


# Create your views here.

@cache_control(max_age=0, no_cache=True, no_store=True, must_revalidate=True)
def index(request):
    games = Product.objects.filter(approved=True).order_by("-popularity").all()
    popularCutoff = games.filter(popularity__gte=POPULARITYCUTOFF).order_by("?")[:3]
    return render(request, "index.html", {"games": games, "cutoff": popularCutoff})


def register(request):
    form_data = BuyerForm()

    if request.POST:

        form_data = BuyerForm(data=request.POST)
        if form_data.is_valid():
            user = User(username=form_data.cleaned_data["username"],
                        email=form_data.cleaned_data["email"].lower(),
                        password=hashers.make_password(form_data.cleaned_data["password"])
                        )
            send_mail("Креиран е нов профил", f"Креиран е профил со корисничко име {user.username}",
                      "arsovskigames@gmail.com", [user.email])
            user.save()
            buyerUser = BuyerUser(user=user)
            buyerUser.save()
            return render(request, "info.html",
                          context=infoContext(request, "Успешно креиран профил! Испратен Ви е мејл. Логирај се", 'success',
                                              '/accounts/login/     '))

    # form.add_error(field=None, error="Invalid Username")
    return render(request, "registration/register.html", context={'registerForm': form_data})


@login_required()
def profile(request, username=None):
    if username is None:
        username = request.user.username
    buyer = BuyerUser.objects.get(user__username=username)
    isDeveloper = False
    if DeveloperUser.objects.filter(user=request.user):
        isDeveloper = True

    form = None
    if request.user.id == buyer.user.id:
        instance = buyer
        form = UserPictureUpdateForm(request.POST or None, request.FILES or None, instance=instance)
        if request.POST and form.is_valid():
            print(request.FILES)
            form.save()
            return redirect("/profile/")

    games = buyer.games.all()

    return render(request, "profile.html", context={"isDev": isDeveloper, "buyer": buyer, "games": games, "form": form})


def product(request, developer, id):
    game = Product.objects.get(id=id)
    tags = game.tags.order_by("-importance").all()[:5]
    images = game.productimage_set.all()
    owned = False
    if not request.user.is_anonymous:
        buyer = BuyerUser.objects.get(user=request.user)

        if buyer.games.contains(game):
            owned = True

    tagForm = TagForm()

    return render(request, "gameView.html",
                  context={"game": game, "tags": tags, "images": images, "owned": owned, "form": tagForm})


@login_required()
def developerTransition(request):
    if not DeveloperUser.objects.filter(user=request.user).exists():
        bUser = BuyerUser.objects.get(user=request.user)

        DeveloperUser(buyeruser_ptr=bUser).save_base(raw=True)

    return redirect(f"/profile/u/{request.user.username}")


@login_required()
def developerGames(request):
    if not DeveloperUser.objects.filter(user=request.user).exists():
        redirect("/")

    games = Product.objects.filter(developer__user=request.user).order_by("-popularity").all()

    paginator = Paginator(games, PAGINATIONSIZE)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    num_pages = paginator.num_pages

    return render(request, "gameList.html",
                  {"page_obj": page_obj, "num_pages": range(1, num_pages + 1), "developerView": True})


@login_required()
def cart(request):
    return render(request, "cart.html")


def gameList(request):
    if request.GET.get('valname'):
        valname = request.GET.get('valname')
        id = \
            Product.objects.filter(approved=True).filter(name=valname).order_by("-popularity")[:LIMITSEARCH].values(
                "name")[
                0][
                'name']
        return JsonResponse({'id': id}, status=200)

    typeSort = request.GET.get("typeSort")

    stringSort = None

    if typeSort == None or typeSort == "p":
        stringSort = "-popularity"
    elif typeSort == "pa":
        stringSort = "price_with_discount"
    elif typeSort == 'pd':
        stringSort = "-price_with_discount"
    elif typeSort == "na":
        stringSort = "name"
    elif typeSort == "nd":
        stringSort = "-name"
    else:
        stringSort = "-popularity"

    print(stringSort)

    searchName = request.GET.get("productName")
    games = None
    if searchName is not None:
        games = Product.objects.filter(approved=True).filter(
            Q(name=searchName) | Q(developer__user__username__icontains=searchName) | Q(
                tags__name__contains=searchName)).annotate(
            price_with_discount=models.ExpressionWrapper(
                models.F('price') - (models.F('price') * models.F('discount') / 100),
                output_field=models.DecimalField(max_digits=10, decimal_places=2)
            )
        ).distinct().order_by(stringSort).all()
    else:
        games = Product.objects.filter(approved=True).annotate(
            price_with_discount=models.ExpressionWrapper(
                models.F('price') - (models.F('price') * models.F('discount') / 100),
                output_field=models.DecimalField(max_digits=10, decimal_places=2)
            )
        ).order_by(stringSort).all()

    f = ProductFilter(request.GET, games)

    paginator = Paginator(f.qs, PAGINATIONSIZE)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    num_pages = paginator.num_pages

    return render(request, "gameList.html",
                  {"page_obj": page_obj, "num_pages": range(1, num_pages + 1), "developerView": False, "filter": f,
                   "sort": typeSort})


@login_required()
def checkout(request):
    if request.POST:

        game_id = request.POST.get("game")
        game = Product.objects.get(id=game_id)
        buyer = BuyerUser.objects.get(user=request.user)
        if buyer.games.filter(id=game.id).exists():
            return render(request, "info.html", context=infoContext(request, "Играта е веќе купена!", 'danger', '/'))

        return render(request, "cart.html", context={"game": game})
    return redirect("/")


@login_required()
def finishCheckout(request):
    if request.POST:
        game_id = request.POST.get("game")

        game = Product.objects.get(id=game_id)
        buyer = BuyerUser.objects.get(user=request.user)
        buyer.games.add(game)

        return render(request, "info.html", context=infoContext(request, "Играта е купена!", 'success', '/profile/'))

    return redirect("/")


@login_required()
def addGame(request):
    form = ProductForm()
    pForm = ImageFormSet(prefix='images')

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        pForm = ImageFormSet(request.POST, request.FILES, prefix='images')

        if form.is_valid() and pForm.is_valid():

            product = form.save(commit=False)
            product.developer = DeveloperUser.objects.get(user=request.user)
            product.popularity = 1
            product.approved = False
            product.save()

            instances = pForm.save(commit=False)
            for instance in instances:
                instance.product = product
                instance.save()

            pForm.save_m2m()
            return redirect('/profile/developer/games')  # Redirect to a success page
    return render(request, "addGame.html", context={"form": form, "pForm": pForm})


@login_required()
def download(request, id):
    buyer = BuyerUser.objects.get(user=request.user)

    if buyer.games.filter(id=id).exists():
        game = Product.objects.get(id=id)
        file_handle = game.files.open()

        response = FileResponse(file_handle, content_type="application/zip")
        response['Content-Length'] = game.files.size
        response['Content-Disposition'] = 'attachment; filename="%s"' % game.files.name
        return response
    else:
        return redirect('/')


def search(request):
    name = request.GET.get("query")

    list = []

    if name:
        games = Product.objects.filter(Q(name__icontains=name) | Q(developer__user__username__icontains=name)).filter(
            approved=True).order_by("-popularity")[:LIMITSEARCH]
        for game in games:
            list.append({"name": game.name, "img": game.titleImage.url, "id": game.id,
                         "developer": game.developer.user.username, "price": game.price_with_discount()})

    return JsonResponse({'status': 200, 'query': list})


def postTag(request):
    if request.method == "POST":
        body = request.body
        decoded = json.loads(body)

        gameid = decoded[0]['game']
        tagName = decoded[1]['tag']
        tag = Tag.objects.filter(product__id=gameid).get_or_create(name__iexact=tagName)[0]
        tag.name = tagName
        tag.importance += 1
        tag.product_set.add(Product.objects.get(id=gameid))
        tag.save(update_fields=["name", "importance"])

        tags = Tag.objects.filter(product__id=gameid).all()

        return JsonResponse({'tags': list(tags.values_list("name", flat=True))}, status=200)
