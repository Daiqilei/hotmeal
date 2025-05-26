# -*- coding: utf-8 -*-
"""
@File       : test_log_output.py
@Date       : 2025-03-01
@Desc       : 测试日志输出


"""

import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def test_log_demo(app):
    logger.info("【/api/v1】这是测试里的日志")
    assert logger.level == logging.INFO or logger.isEnabledFor(logging.INFO)
    assert True
