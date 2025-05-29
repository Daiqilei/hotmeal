# -*- coding: utf-8 -*-
"""
@file         tests/test_tag.py
@description  测试tag模块
@date         2025-05-29
@author       taichilei
"""

import pytest

from app import create_app
from app.models.tag import Tag
from app.services.tag_service import create_tag, update_tag


@pytest.fixture(scope='module')
def app():
    """
    Create a new app instance for each test
    """
    app = create_app('testing')
    with app.app_context():
        yield app


@pytest.fixture(scope='function')
def db(app):
    """
    Create a new database for each test
    """
    from app import db as _db  # ✅ 确保使用已注册的 db 实例
    with app.app_context():
        _db.create_all()
        yield _db
        _db.session.remove()
        _db.drop_all()


@pytest.fixture
def sample_tag(app, db):
    """
    Create a sample tag with name 'New'
    """
    with app.app_context():
        from app import db as _db
        _db.session.query(Tag).filter(Tag.name.in_(['New', 'new'])).delete()
        _db.session.commit()
        tag = create_tag('New')
        yield tag
        _db.session.query(Tag).filter_by(tag_id=tag.tag_id).delete()
        _db.session.commit()


def test_update_tag_case_insensitive(app, db, sample_tag):
    with app.app_context():
        tag_id = sample_tag.tag_id
        assert sample_tag.name == 'New'
        updated_tag = update_tag(tag_id, 'new')
        from_db = Tag.query.get(tag_id)
        assert from_db.name == 'new'
        assert updated_tag.name == 'new'
