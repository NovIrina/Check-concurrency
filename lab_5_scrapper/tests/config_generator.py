# pylint: disable=too-many-arguments
"""
Generates config with flexible params for testing purposes
"""
import json
import shutil
from pathlib import Path

from config.test_params import TEST_CRAWLER_CONFIG_PATH, TEST_PATH


def generate_config(seed_urls: list,
                    num_articles: int,
                    headers: dict[str, str],
                    encoding: str,
                    timeout: int,
                    should_verify_certificate: bool,
                    headless_mode: bool,
                    path: Path = TEST_CRAWLER_CONFIG_PATH):
    """
    Generates scrapper_config.py for testing
    """
    config = {'seed_urls': seed_urls,
              'total_articles_to_find_and_parse': num_articles,
              'headers': headers,
              'encoding': encoding,
              'timeout': timeout,
              'should_verify_certificate': should_verify_certificate,
              'headless_mode': headless_mode}

    if path.exists():
        shutil.rmtree(TEST_PATH)
    TEST_PATH.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding='utf-8') as file:
        json.dump(config, file)
