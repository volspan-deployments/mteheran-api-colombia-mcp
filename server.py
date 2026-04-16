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
    "tourist_attractions": "touristattraction",
    "natural_areas": "naturalarea",
    "typical_dishes": "typicaldish",
    "fairs_festivals": "fairfestival",
    "intangible_heritage": "intangibleheritage",
    "maps": "map",
}

INDIGENOUS_CATEGORY_MAP = {
    "indigenous_reservations": "indigenousreservation",
    "native_communities": "nativecommunity",
    "invasive_species": "invasivespecies",
    "radio_stations": "radiostation",
    "constitution_articles": "constitutionarticle",
}


@mcp.tool()
async def get_country_info() -> dict:
    """Retrieve general information about Colombia as a country, such as capital, population, area, official language, currency, and other national facts."""
    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.get(f"{BASE_URL}/country/Colombia")
        if response.status_code == 200:
            return {"success": True, "data": response.json()}
        # Fallback: try the country list endpoint
        response = await client.get(f"{BASE_URL}/country")
        if response.status_code == 200:
            return {"success": True, "data": response.json()}
        return {"success": False, "status_code": response.status_code, "error": response.text}


@mcp.tool()
async def get_departments(
    id: Optional[int] = None,
    name: Optional[str] = None
) -> dict:
    """Retrieve a list of all departments (states/regions) of Colombia, or get detailed information about a specific department by its ID or name."""
    async with httpx.AsyncClient(timeout=30) as client:
        if id is not None:
            response = await client.get(f"{BASE_URL}/department/{id}")
            if response.status_code == 200:
                return {"success": True, "data": response.json()}
            return {"success": False, "status_code": response.status_code, "error": response.text}

        if name:
            response = await client.get(f"{BASE_URL}/department/search/{name}")
            if response.status_code == 200:
                return {"success": True, "data": response.json()}
            return {"success": False, "status_code": response.status_code, "error": response.text}

        response = await client.get(f"{BASE_URL}/department")
        if response.status_code == 200:
            return {"success": True, "data": response.json()}
        return {"success": False, "status_code": response.status_code, "error": response.text}


@mcp.tool()
async def get_cities(
    id: Optional[int] = None,
    department_id: Optional[int] = None,
    name: Optional[str] = None
) -> dict:
    """Retrieve a list of cities in Colombia, optionally filtered by department or searched by name."""
    async with httpx.AsyncClient(timeout=30) as client:
        if id is not None:
            response = await client.get(f"{BASE_URL}/city/{id}")
            if response.status_code == 200:
                return {"success": True, "data": response.json()}
            return {"success": False, "status_code": response.status_code, "error": response.text}

        if department_id is not None:
            response = await client.get(f"{BASE_URL}/department/{department_id}/cities")
            if response.status_code == 200:
                return {"success": True, "data": response.json()}
            return {"success": False, "status_code": response.status_code, "error": response.text}

        if name:
            response = await client.get(f"{BASE_URL}/city/search/{name}")
            if response.status_code == 200:
                return {"success": True, "data": response.json()}
            return {"success": False, "status_code": response.status_code, "error": response.text}

        response = await client.get(f"{BASE_URL}/city")
        if response.status_code == 200:
            return {"success": True, "data": response.json()}
        return {"success": False, "status_code": response.status_code, "error": response.text}


@mcp.tool()
async def get_presidents(
    id: Optional[int] = None,
    name: Optional[str] = None
) -> dict:
    """Retrieve information about Colombian presidents, including historical and current ones. Can fetch all presidents or a specific one by ID or name."""
    async with httpx.AsyncClient(timeout=30) as client:
        if id is not None:
            response = await client.get(f"{BASE_URL}/president/{id}")
            if response.status_code == 200:
                return {"success": True, "data": response.json()}
            return {"success": False, "status_code": response.status_code, "error": response.text}

        if name:
            response = await client.get(f"{BASE_URL}/president/search/{name}")
            if response.status_code == 200:
                return {"success": True, "data": response.json()}
            return {"success": False, "status_code": response.status_code, "error": response.text}

        response = await client.get(f"{BASE_URL}/president")
        if response.status_code == 200:
            return {"success": True, "data": response.json()}
        return {"success": False, "status_code": response.status_code, "error": response.text}


@mcp.tool()
async def get_tourist_attractions(
    category: str,
    id: Optional[int] = None,
    name: Optional[str] = None,
    department_id: Optional[int] = None
) -> dict:
    """Retrieve information about tourist attractions, natural areas, typical dishes, traditional fairs, intangible heritage, or maps in Colombia.
    Category accepted values: 'tourist_attractions', 'natural_areas', 'typical_dishes', 'fairs_festivals', 'intangible_heritage', 'maps'."""
    endpoint = CATEGORY_MAP.get(category)
    if not endpoint:
        return {
            "success": False,
            "error": f"Invalid category '{category}'. Accepted values: {list(CATEGORY_MAP.keys())}"
        }

    async with httpx.AsyncClient(timeout=30) as client:
        if id is not None:
            response = await client.get(f"{BASE_URL}/{endpoint}/{id}")
            if response.status_code == 200:
                return {"success": True, "data": response.json()}
            return {"success": False, "status_code": response.status_code, "error": response.text}

        if department_id is not None:
            response = await client.get(f"{BASE_URL}/department/{department_id}/{endpoint}")
            if response.status_code == 200:
                return {"success": True, "data": response.json()}
            # Fallback: get all and note department_id filtering not supported
            return {"success": False, "status_code": response.status_code, "error": response.text}

        if name:
            response = await client.get(f"{BASE_URL}/{endpoint}/search/{name}")
            if response.status_code == 200:
                return {"success": True, "data": response.json()}
            return {"success": False, "status_code": response.status_code, "error": response.text}

        response = await client.get(f"{BASE_URL}/{endpoint}")
        if response.status_code == 200:
            return {"success": True, "data": response.json()}
        return {"success": False, "status_code": response.status_code, "error": response.text}


@mcp.tool()
async def get_airports(
    id: Optional[int] = None,
    name: Optional[str] = None,
    department_id: Optional[int] = None
) -> dict:
    """Retrieve information about airports in Colombia, including location, type, and IATA codes."""
    async with httpx.AsyncClient(timeout=30) as client:
        if id is not None:
            response = await client.get(f"{BASE_URL}/airport/{id}")
            if response.status_code == 200:
                return {"success": True, "data": response.json()}
            return {"success": False, "status_code": response.status_code, "error": response.text}

        if department_id is not None:
            response = await client.get(f"{BASE_URL}/department/{department_id}/airports")
            if response.status_code == 200:
                return {"success": True, "data": response.json()}
            return {"success": False, "status_code": response.status_code, "error": response.text}

        if name:
            response = await client.get(f"{BASE_URL}/airport/search/{name}")
            if response.status_code == 200:
                return {"success": True, "data": response.json()}
            return {"success": False, "status_code": response.status_code, "error": response.text}

        response = await client.get(f"{BASE_URL}/airport")
        if response.status_code == 200:
            return {"success": True, "data": response.json()}
        return {"success": False, "status_code": response.status_code, "error": response.text}


@mcp.tool()
async def get_holidays(
    year: Optional[int] = None
) -> dict:
    """Retrieve public holidays in Colombia for a specific year or all available data."""
    async with httpx.AsyncClient(timeout=30) as client:
        if year is not None:
            response = await client.get(f"{BASE_URL}/holiday/{year}")
            if response.status_code == 200:
                return {"success": True, "year": year, "data": response.json()}
            return {"success": False, "status_code": response.status_code, "error": response.text}

        response = await client.get(f"{BASE_URL}/holiday")
        if response.status_code == 200:
            return {"success": True, "data": response.json()}
        return {"success": False, "status_code": response.status_code, "error": response.text}


@mcp.tool()
async def get_indigenous_communities(
    category: str,
    id: Optional[int] = None,
    name: Optional[str] = None,
    department_id: Optional[int] = None
) -> dict:
    """Retrieve information about indigenous communities, reservations, invasive species, radio stations, native communities, or constitution articles in Colombia.
    Category accepted values: 'indigenous_reservations', 'native_communities', 'invasive_species', 'radio_stations', 'constitution_articles'."""
    endpoint = INDIGENOUS_CATEGORY_MAP.get(category)
    if not endpoint:
        return {
            "success": False,
            "error": f"Invalid category '{category}'. Accepted values: {list(INDIGENOUS_CATEGORY_MAP.keys())}"
        }

    async with httpx.AsyncClient(timeout=30) as client:
        if id is not None:
            response = await client.get(f"{BASE_URL}/{endpoint}/{id}")
            if response.status_code == 200:
                return {"success": True, "data": response.json()}
            return {"success": False, "status_code": response.status_code, "error": response.text}

        if department_id is not None:
            response = await client.get(f"{BASE_URL}/department/{department_id}/{endpoint}")
            if response.status_code == 200:
                return {"success": True, "data": response.json()}
            # Fallback to search all
            return {"success": False, "status_code": response.status_code, "error": response.text}

        if name:
            response = await client.get(f"{BASE_URL}/{endpoint}/search/{name}")
            if response.status_code == 200:
                return {"success": True, "data": response.json()}
            return {"success": False, "status_code": response.status_code, "error": response.text}

        response = await client.get(f"{BASE_URL}/{endpoint}")
        if response.status_code == 200:
            return {"success": True, "data": response.json()}
        return {"success": False, "status_code": response.status_code, "error": response.text}




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
