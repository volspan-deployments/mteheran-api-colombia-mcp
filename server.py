from starlette.applications import Starlette
from starlette.routing import Route, Mount
from starlette.responses import JSONResponse
import uvicorn
import threading
from fastmcp import FastMCP
import httpx
import os
from typing import Optional

mcp = FastMCP("API Colombia")

BASE_URL = "https://api-colombia.com/api/v1"

CATEGORY_MAP = {
    "natural_areas": "NaturalArea",
    "radio_stations": "RadioStation",
    "typical_dishes": "TypicalDish",
    "fairs_festivals": "TouristicFairFestival",
    "intangible_heritage": "IntangibleHeritage",
    "indigenous_reservations": "IndigenousReservation",
    "native_communities": "NativeCommunity",
    "invasive_species": "InvasiveSpecies",
    "constitution_articles": "ConstitutionArticle",
    "maps": "Map",
}


@mcp.tool()
async def get_country_info() -> dict:
    """Retrieve general information about Colombia as a country, including capital, population, area, currency, language, and other national facts."""
    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.get(f"{BASE_URL}/Country/Colombia")
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def get_departments(
    id: Optional[int] = None,
    name: Optional[str] = None
) -> dict:
    """Retrieve a list of all departments (states/provinces) of Colombia, or get details about a specific department by its ID or name."""
    async with httpx.AsyncClient(timeout=30) as client:
        if id is not None:
            response = await client.get(f"{BASE_URL}/Department/{id}")
            response.raise_for_status()
            return response.json()
        elif name:
            response = await client.get(f"{BASE_URL}/Department/search/{name}")
            response.raise_for_status()
            return {"results": response.json()}
        else:
            response = await client.get(f"{BASE_URL}/Department")
            response.raise_for_status()
            return {"results": response.json()}


@mcp.tool()
async def get_cities(
    id: Optional[int] = None,
    name: Optional[str] = None,
    department_id: Optional[int] = None
) -> dict:
    """Retrieve a list of all cities in Colombia, get a specific city by ID, search cities by name, or filter by department ID."""
    async with httpx.AsyncClient(timeout=30) as client:
        if id is not None:
            response = await client.get(f"{BASE_URL}/City/{id}")
            response.raise_for_status()
            return response.json()
        elif name:
            response = await client.get(f"{BASE_URL}/City/search/{name}")
            response.raise_for_status()
            return {"results": response.json()}
        elif department_id is not None:
            response = await client.get(f"{BASE_URL}/Department/{department_id}/cities")
            response.raise_for_status()
            return {"results": response.json()}
        else:
            response = await client.get(f"{BASE_URL}/City")
            response.raise_for_status()
            return {"results": response.json()}


@mcp.tool()
async def get_presidents(
    id: Optional[int] = None,
    name: Optional[str] = None
) -> dict:
    """Retrieve a list of all Colombian presidents throughout history, or get details about a specific president by ID or search by name."""
    async with httpx.AsyncClient(timeout=30) as client:
        if id is not None:
            response = await client.get(f"{BASE_URL}/President/{id}")
            response.raise_for_status()
            return response.json()
        elif name:
            response = await client.get(f"{BASE_URL}/President/search/{name}")
            response.raise_for_status()
            return {"results": response.json()}
        else:
            response = await client.get(f"{BASE_URL}/President")
            response.raise_for_status()
            return {"results": response.json()}


@mcp.tool()
async def get_tourist_attractions(
    id: Optional[int] = None,
    city_id: Optional[int] = None,
    name: Optional[str] = None
) -> dict:
    """Retrieve tourist attractions in Colombia, optionally filtered by city or searched by name."""
    async with httpx.AsyncClient(timeout=30) as client:
        if id is not None:
            response = await client.get(f"{BASE_URL}/TouristicAttraction/{id}")
            response.raise_for_status()
            return response.json()
        elif name:
            response = await client.get(f"{BASE_URL}/TouristicAttraction/search/{name}")
            response.raise_for_status()
            return {"results": response.json()}
        elif city_id is not None:
            response = await client.get(f"{BASE_URL}/City/{city_id}/touristicattractions")
            response.raise_for_status()
            return {"results": response.json()}
        else:
            response = await client.get(f"{BASE_URL}/TouristicAttraction")
            response.raise_for_status()
            return {"results": response.json()}


@mcp.tool()
async def get_holidays(
    year: Optional[int] = None
) -> dict:
    """Retrieve Colombian public holidays, optionally filtered by year."""
    async with httpx.AsyncClient(timeout=30) as client:
        if year is not None:
            response = await client.get(f"{BASE_URL}/Holiday/{year}")
            response.raise_for_status()
            return {"year": year, "results": response.json()}
        else:
            response = await client.get(f"{BASE_URL}/Holiday")
            response.raise_for_status()
            return {"results": response.json()}


@mcp.tool()
async def get_airports(
    id: Optional[int] = None,
    name: Optional[str] = None,
    city_id: Optional[int] = None
) -> dict:
    """Retrieve information about airports in Colombia, including location, IATA code, and type. Can filter by city or search by name."""
    async with httpx.AsyncClient(timeout=30) as client:
        if id is not None:
            response = await client.get(f"{BASE_URL}/Airport/{id}")
            response.raise_for_status()
            return response.json()
        elif name:
            response = await client.get(f"{BASE_URL}/Airport/search/{name}")
            response.raise_for_status()
            return {"results": response.json()}
        elif city_id is not None:
            response = await client.get(f"{BASE_URL}/City/{city_id}/airports")
            response.raise_for_status()
            return {"results": response.json()}
        else:
            response = await client.get(f"{BASE_URL}/Airport")
            response.raise_for_status()
            return {"results": response.json()}


@mcp.tool()
async def get_cultural_info(
    category: str,
    id: Optional[int] = None,
    name: Optional[str] = None
) -> dict:
    """Retrieve various cultural and natural data about Colombia. Category must be one of: 'natural_areas', 'radio_stations', 'typical_dishes', 'fairs_festivals', 'intangible_heritage', 'indigenous_reservations', 'native_communities', 'invasive_species', 'constitution_articles', 'maps'."""
    if category not in CATEGORY_MAP:
        return {
            "error": f"Invalid category '{category}'. Must be one of: {', '.join(CATEGORY_MAP.keys())}"
        }
    endpoint = CATEGORY_MAP[category]
    async with httpx.AsyncClient(timeout=30) as client:
        if id is not None:
            response = await client.get(f"{BASE_URL}/{endpoint}/{id}")
            response.raise_for_status()
            return response.json()
        elif name:
            response = await client.get(f"{BASE_URL}/{endpoint}/search/{name}")
            response.raise_for_status()
            return {"category": category, "results": response.json()}
        else:
            response = await client.get(f"{BASE_URL}/{endpoint}")
            response.raise_for_status()
            return {"category": category, "results": response.json()}




_SERVER_SLUG = "mteheran-api-colombia"

def _track(tool_name: str, ua: str = ""):
    try:
        import urllib.request, json as _json
        data = _json.dumps({"slug": _SERVER_SLUG, "event": "tool_call", "tool": tool_name, "user_agent": ua}).encode()
        req = urllib.request.Request("https://www.volspan.dev/api/analytics/event", data=data, headers={"Content-Type": "application/json"})
        urllib.request.urlopen(req, timeout=1)
    except Exception:
        pass

async def health(request):
    return JSONResponse({"status": "ok", "server": mcp.name})

async def tools(request):
    registered = await mcp.list_tools()
    tool_list = [{"name": t.name, "description": t.description or ""} for t in registered]
    return JSONResponse({"tools": tool_list, "count": len(tool_list)})

sse_app = mcp.http_app(transport="sse")

app = Starlette(
    routes=[
        Route("/health", health),
        Route("/tools", tools),
        Mount("/", sse_app),
    ],
    lifespan=sse_app.lifespan,
)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
