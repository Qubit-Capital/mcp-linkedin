from fastmcp import FastMCP
from typing import List, Dict, Optional, Any
import http.client
import json
import os
import urllib.parse
import logging
import traceback
import time
from starlette.responses import JSONResponse

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('linkedin_api_tools')

# Create MCP server
mcp = FastMCP("LinkedInProfiler", stateless_http=True)
app = mcp.http_app(path="/linkedin")

# API config from environment
LINKEDIN_API_KEY = os.environ.get("LINKEDIN_API_KEY")
LINKEDIN_API_HOST = "linkedin-bulk-data-scraper.p.rapidapi.com"
LINKEDIN_API_USER = os.environ.get("LINKEDIN_API_USER", "usama")

if not LINKEDIN_API_KEY:
    logger.error("Missing LINKEDIN_API_KEY environment variable")
    raise RuntimeError("LINKEDIN_API_KEY is required")

@app.route("/", methods=["GET"])
async def alive(request):
    return JSONResponse({"status": "ok"})

# LinkedIn API headers
def get_linkedin_headers() -> Dict:
    return {
        "Content-Type": "application/json",
        "x-rapidapi-host": LINKEDIN_API_HOST,
        "x-rapidapi-key": LINKEDIN_API_KEY,
        "x-rapidapi-user": LINKEDIN_API_USER
    }

# Helper function for making API requests with error handling
def make_api_request(method: str, endpoint: str, payload: Optional[str] = None) -> Dict[str, Any]:
    MAX_RETRIES = 3
    RETRY_DELAY = 2

    headers = get_linkedin_headers()
    sanitized_headers = {k: v for k, v in headers.items() if k.lower() != 'x-rapidapi-key'}

    logger.info(f"API Request: {method} {endpoint}")
    logger.debug(f"Headers: {sanitized_headers}")

    if payload:
        logger.debug(f"Payload: {payload[:200]}..." if len(payload) > 200 else f"Payload: {payload}")

    for attempt in range(MAX_RETRIES):
        try:
            conn = http.client.HTTPSConnection(LINKEDIN_API_HOST, timeout=30)
            conn.request(method, endpoint, payload, headers)
            res = conn.getresponse()
            data = res.read().decode("utf-8")
            logger.info(f"API Response: {method} {endpoint} - Status: {res.status}")

            if data:
                try:
                    response_data = json.loads(data)
                    if res.status >= 400:
                        error_msg = response_data.get('message', 'Unknown API error')
                        return {
                            "success": False,
                            "status": res.status,
                            "message": error_msg,
                            "details": response_data
                        }
                    return {
                        "success": True,
                        "status": res.status,
                        "data": response_data
                    }
                except json.JSONDecodeError as e:
                    return {
                        "success": False,
                        "status": res.status,
                        "message": "Failed to decode JSON response",
                        "details": {"error": str(e), "raw_data": data}
                    }
            else:
                return {
                    "success": False,
                    "status": res.status,
                    "message": "Empty response from API"
                }
        except Exception as e:
            logger.error(f"Request Error: {method} {endpoint} - {str(e)}")
            if attempt < MAX_RETRIES - 1:
                time.sleep(RETRY_DELAY * (attempt + 1))
            else:
                return {
                    "success": False,
                    "status": 500,
                    "message": f"Request failed after {MAX_RETRIES} attempts",
                    "details": {"error": str(e)}
                }
        finally:
            if 'conn' in locals():
                conn.close()

# Tools
@mcp.tool()
def profiles(links: List[str]) -> Dict:
    try:
        payload = json.dumps({"links": links})
        return make_api_request("POST", "/profiles", payload)
    except Exception as e:
        return {"error": str(e), "exception_type": type(e).__name__}

@mcp.tool()
def companies(links: List[str]) -> Dict:
    try:
        payload = json.dumps({"links": links})
        return make_api_request("POST", "/companies", payload)
    except Exception as e:
        return {"error": str(e), "exception_type": type(e).__name__}

@mcp.tool()
def company_posts(links: List[str], count: int = 1) -> Dict:
    try:
        payload = json.dumps({"links": links, "count": count})
        return make_api_request("POST", "/company_posts", payload)
    except Exception as e:
        return {"error": str(e), "exception_type": type(e).__name__}

@mcp.tool()
def person(link: str) -> Dict:
    try:
        payload = json.dumps({"link": link})
        return make_api_request("POST", "/person", payload)
    except Exception as e:
        return {"error": str(e), "exception_type": type(e).__name__}
