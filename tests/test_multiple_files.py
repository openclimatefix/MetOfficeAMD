import tempfile
from unittest import mock

import xarray as xr

from metofficedatahub.multiple_files import MetOfficeDataHub, save_to_zarr
from tests.conftest import mocked_requests_get


def test_init():
    _ = MetOfficeDataHub(client_id="fake", client_secret="fake")


@mock.patch("requests.get", side_effect=mocked_requests_get)
def test_download_all_none(mock_get):
    """Check that if there are no order ids, then no data is downloaded"""
    datahub = MetOfficeDataHub(client_id="fake", client_secret="fake")
    datahub.download_all_files(order_ids=[])


@mock.patch("requests.get", side_effect=mocked_requests_get)
def test_download_all(mock_get):
    """Check that if there are no order ids, then no data is downloaded"""
    datahub = MetOfficeDataHub(client_id="fake", client_secret="fake")

    datahub.download_all_files(order_ids=["test_order_id"])


@mock.patch("requests.get", side_effect=mocked_requests_get)
def test_load_all_files(mock_get):

    datahub = MetOfficeDataHub(client_id="fake", client_secret="fake")
    datahub.download_all_files(order_ids=["test_order_id"])
    data = datahub.load_all_files()
    assert type(data) == xr.Dataset


@mock.patch("requests.get", side_effect=mocked_requests_get)
def test_save_to_zarr(mock_get):

    datahub = MetOfficeDataHub(client_id="fake", client_secret="fake")
    datahub.download_all_files(order_ids=["test_order_id"])
    data = datahub.load_all_files()

    with tempfile.TemporaryDirectory() as tmpdirname:
        save_to_zarr(data, save_dir=tmpdirname)
