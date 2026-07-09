"""
POST /api/search - kick off a scrape run for chosen industries/regions.

For now this runs synchronously and returns leads directly. Once the
scraper is real (and slow, given rate limiting), swap this for a
background task (FastAPI BackgroundTasks or a task queue) and have the
frontend poll a /status endpoint - that's what the "progress indicator"
in the React dashboard will hook into.
"""

from fastapi import APIRouter
from pydantic import BaseModel
from typing import List

from scraper.maps_scraper import run_maps_scrape
from scraper.directory_scraper import run_directory_scrape

router = APIRouter()


class SearchRequest(BaseModel):
    regions: List[str]
    include_maps: bool = True
    include_directories: bool = True


@router.post("/")
def start_search(payload: SearchRequest):
    leads = []

    if payload.include_maps:
        leads.extend(run_maps_scrape(regions=payload.regions))

    if payload.include_directories:
        for region in payload.regions:
            leads.extend(run_directory_scrape(region))

    # TODO: save `leads` to DB via SQLAlchemy session (see database.py)
    return {"count": len(leads), "leads": leads}
