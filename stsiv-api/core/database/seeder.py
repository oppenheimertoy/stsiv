"""
Module contains Seeder class realization
"""
import logging
from typing import Dict, Any
from typing import List
import json
from core.repository.base_repo import AsyncBaseRepository
from core.config import config

logging.basicConfig(level=logging.INFO)


class Seeder():
    """
    Seeder class for creating seeds in categories table
    """
    paths_to_seeds = config.SEED_PATHS.split(",")

    def __init__(self, repos: List[AsyncBaseRepository]) -> None:
        self.repos = repos

    async def create_seeds(self) -> None:
        """
        Creating seeds exsisting in /seeds directory
        """
        for repo_type, seed in zip(self.repos, self._parse_json_seeds()):
            for item in seed:
                if not await repo_type.async_exists(item):
                    await repo_type.async_create(**item)
                    logging.info("Successfully inserted new item \
                            <%(identifier)s,%(name)s>", item)

    def _parse_json_seeds(self) -> List[List[Dict[str, Any]]]:
        """
        Parsing data from .json files in seeds directory
        Returns:
            List[List[Dict[str, Any]]]: 
        """
        seeds_list = []
        for path in self.paths_to_seeds:
            try:
                with open(str(path), "r", encoding="utf-8") as json_file:
                    seeds_list.append(json.loads(json_file.read())["items"])
            except (FileNotFoundError, json.JSONDecodeError) as exc:
                logging.error("An error occurred: %e", exc)
        return seeds_list
