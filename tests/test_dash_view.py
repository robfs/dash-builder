"""Tests for the DashView class."""

import pytest
from dash import ALL, MATCH

from src.dash_builder import DashView


def test_view_name(test_view):
    assert test_view.name() == "test-view"


def test_view_name_with_sub_name(test_view):
    assert test_view.name("sub") == "test-view-sub"


def test_view_id(test_view):
    assert test_view.id("test-id") == {"type": "test-view", "index": "test-id"}


def test_view_matched_id(test_view):
    assert test_view.matched_id() == {"type": "test-view", "index": MATCH}


def test_view_all_ids(test_view):
    assert test_view.all_ids() == {"type": "test-view", "index": ALL}


def test_abstract_view_raises():
    with pytest.raises(TypeError):
        DashView()


def test_abstract_create_raises():
    with pytest.raises(NotImplementedError):
        DashView.valid_layout("test-id")
