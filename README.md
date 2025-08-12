# LinkedIn MCP Server

A Model Context Protocol (MCP) server that provides LinkedIn profile and company data scraping capabilities through a FastAPI-based web service.

## Features

- **LinkedIn Profile Scraping**: Fetch detailed profile information from LinkedIn URLs
- **Company Data**: Retrieve company information and recent posts
- **Bulk Operations**: Process multiple LinkedIn links in a single request
- **Health Monitoring**: Built-in health check endpoints
- **Error Handling**: Robust error handling with retry logic

## Prerequisites

- Python 3.11 or higher
- LinkedIn API key from RapidAPI

## Setup

1. **Clone the repository**:

   ```bash
   git clone <repository-url>
   cd mcp-linkedin
   ```

2. **Create a virtual environment**:

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   ```bash
   export LINKEDIN_API_KEY="your_rapidapi_key_here"
   export LINKEDIN_API_USER="your_username"  # Optional, defaults to "usama"
   ```

## Running the Server

### Development Mode

```bash
source venv/bin/activate
python main.py
```

### Docker Mode

```bash
docker build -t linkedin-mcp .
docker run -p 8080:8080 -e LINKEDIN_API_KEY="your_key" linkedin-mcp
```

The server will start on `http://localhost:8080`

## API Endpoints

### Health Check

- `GET /health` - Server health status
- `GET /` - Root endpoint with basic info

### MCP Tools

- `profiles(links: List[str])` - Fetch LinkedIn profile data
- `companies(links: List[str])` - Fetch LinkedIn company data
- `company_posts(links: List[str], count: int)` - Fetch recent company posts
- `person(link: str)` - Fetch detailed person/profile data

## Environment Variables

- `LINKEDIN_API_KEY` (required): Your RapidAPI key for LinkedIn data scraping
- `LINKEDIN_API_USER` (optional): API username, defaults to "usama"
- `PORT` (optional): Server port, defaults to 8080

## Example Usage

```python
# Health check
curl http://localhost:8080/health

# Fetch profile data
curl -X POST http://localhost:8080/mcp \
  -H "Content-Type: application/json" \
  -d '{"method": "profiles", "params": {"links": ["https://linkedin.com/in/example"]}}'
```

## Docker

The included Dockerfile creates a lightweight container using Python 3.11 Alpine Linux. The container exposes port 8080 and runs the MCP server automatically.

## License

[Add your license information here]
