"""
Lead Generation Scraper - FastAPI backend entry point.

Run with: uvicorn main:app --reload
Swagger docs available at: http://127.0.0.1:8000/docs
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes import search, results, export

app = FastAPI(
    title="Lead Generation Scraper API",
    description="API for scraping and managing manufacturing leads (pharma + general manufacturing).",
    version="0.1.0",
)

# Allow the React dev server to call this API during development.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(search.router, prefix="/api/search", tags=["search"])
app.include_router(results.router, prefix="/api/results", tags=["results"])
app.include_router(export.router, prefix="/api/export", tags=["export"])


@app.get("/")
def root():
    return {"status": "ok", "message": "Lead Gen Scraper API is running"}
