"""Integration tests between database and server"""
from django.test import RequestFactory, TestCase
from django.contrib.auth.models import AnonymousUser
import sys
import os

from core.models import Tiles as TileTable
from core.models import Objects as ObjectsTable
from core.models import Dataset as DatasetTable

sys.path.append(os.path.join(os.path.dirname("src"), '..'))
# pylint: disable=all


# Create your tests here.
from src.core.views import *


class TestRequests(TestCase):

    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()

        tile_ds = DatasetTable()
        tile_ds.x_coord = 0
        tile_ds.y_coord = 0
        tile_ds.water = 0
        tile_ds.land = 1
        tile_ds.building = 1
        tile_ds.year = 2014
        tile_ds.save()

        tile = TileTable()
        tile.x_coord = 2
        tile.y_coord = 2
        tile.year = 2014
        tile.save()

        stored_tile2 = TileTable.objects.filter(x_coord=2, y_coord=2,
                                                year=2014)

        obj = ObjectsTable()
        obj.tiles_id = stored_tile2[0]
        obj.x_coord = 0
        obj.y_coord = 0
        obj.prediction = 100
        obj.type = 'oiltank'
        obj.save()

    def test_get_statistics(self):
        # Create an instance of a GET request.
        request = self.factory.get('get_statistics_year')

        # an AnonymousUser instance.
        request.user = AnonymousUser()
        response = get_statistics(request)
        self.assertEqual(response.status_code, 200)

    def test_get_statistics_year(self):
        # Create an instance of a GET request.
        request = self.factory.get('get_statistics_year')

        # an AnonymousUser instance.
        request.user = AnonymousUser()
        response = get_statistics_year(request, requested_year=2010)
        self.assertEqual(response.status_code, 200)

    def test_get_markers_no_objects(self):
        # Create an instance of a GET request.
        request = self.factory.get('get_markers')

        # an AnonymousUser instance.
        request.user = AnonymousUser()
        response = get_markers(request)
        self.assertEqual(response.status_code, 200)

    def test_get_markers(self):
        # Create an instance of a GET request.
        request = self.factory.get('get_markers')

        # an AnonymousUser instance.
        request.user = AnonymousUser()
        response = get_markers(request)
        self.assertEqual(response.status_code, 200)

    def test_get_labels_tile_found(self):
        submission = '{"year": 2014, "x_coord": 0, "y_coord": 0}'

        sub = json.loads(submission)
        # Create an instance of a GET request.
        request = self.factory.get('get_labels')

        # an AnonymousUser instance.
        request.user = AnonymousUser()
        response = get_labels(request, submission)
        self.assertEqual(response.status_code, 200)

    def test_get_labels_tile_not_found(self):
        submission = '{"year": 2010, "x_coord": 0, "y_coord": 0}'

        sub = json.loads(submission)
        # Create an instance of a GET request.
        request = self.factory.get('get_labels')

        # an AnonymousUser instance.
        request.user = AnonymousUser()
        response = get_labels(request, submission)
        self.assertEqual(response.status_code, 200)
