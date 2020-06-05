"""Views module"""
# pylint: disable=[line-too-long,import-error, unused-argument, no-name-in-module,wildcard-import, fixme]

import random
import json

from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest

from core.models import CaptchaSubmissions as CaptchaTable
from core.models import Dataset as DatasetTable
from core.models import Tiles as TileTable
from core.models import Characteristics as CharacteristicsTable
from core.captcha import pick_unsolved_captcha, pick_random_captcha, find_tiles, check_characteristics, \
     check_objects


def home(request):
    """render index.html page"""
    return render(request, 'maps/main.html')


def captcha(request):
    """render captcha.html page"""
    return render(request, 'captcha/captcha.html')


def tiles_overview(request):
    """render tiles_overview.html page"""

    return render(request, 'tiles-overview/tiles_overview.html')


def get_statistics(request):
    """send statistics json"""
    # TODO: statistics for ai
    cap = CaptchaTable.objects.all().count()
    dataset = DatasetTable.objects.all().count()
    response = {'ai': 0, 'cap': cap, 'dataset': dataset}
    return JsonResponse(response, safe=False)


def get_statistics_year(request, requested_year):
    """send statistics json by year"""
    # TODO: statistics for ai
    cap = CaptchaTable.objects.filter(year=requested_year).count()
    dataset = DatasetTable.objects.filter(year=requested_year).count()
    response = {'ai': 0, 'cap': cap, 'dataset': dataset}
    return JsonResponse(response, safe=False)


def get_markers(request):
    """Return json array of markers"""
    with open("core/json/points.json", 'r') as markers:
        data = markers.read()
    return JsonResponse(data, safe=False)


def get_tile(request):
    """Return two object containing: year, x, y"""

    (year_new, x_new, y_new) = pick_unsolved_captcha()

    if year_new == -1:  # If all current captchas are solved, pick a random new challenge
        print("Out of challenges. Picking random")
        (year_new, x_new, y_new) = pick_random_captcha()

    # Pick a known tile
    tile = random.choice(TileTable.objects.all())

    year_known = tile.year
    x_known = tile.x_coord
    y_known = tile.y_coord

    response = [{'year': year_new, 'x': x_new, 'y': y_new},
                {'year': year_known, 'x': x_known, 'y': y_known}]
    random.shuffle(response)

    return JsonResponse(response, safe=False)


def submit_captcha(request):
    """Verify captcha challenge"""
    # NOTE: Terrible code ahead. I'll try to make it prettier later on. -Georgi
    submission = json.loads(request.body)
    print(submission)

    # Find which tile is the control
    control = find_tiles(submission)
    if control == 0:
        return HttpResponseBadRequest("No tile")

    control_tile = control[0]
    control_sub = control[1]
    unid_sub = control[2]

    char_query = CharacteristicsTable.objects.filter(tiles_id=control_tile.id)
    if len(char_query) == 0:
        return HttpResponseBadRequest("No characteristics")
    control_char = char_query[0]

    # Check the characteristics
    if check_characteristics(control_sub, control_char):
        if check_objects(control_sub, unid_sub, control_tile):
            return HttpResponse()
    return HttpResponseBadRequest("Wrong answer")
