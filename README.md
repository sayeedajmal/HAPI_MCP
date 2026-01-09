# HAPI FHIR MCP Project

A modular Model Context Protocol (MCP) server for interacting with a HAPI FHIR JPA server. This project allows LLMs (like Claude or ChatGPT) to perform FHIR operations (Patient, Organization, etc.) using user-provided JWT tokens.

## Architecture

The project uses a modular architecture where each FHIR resource type is implemented as a separate module in the `modules/` directory. The `main.py` script serves as the central entry point.

```
HAPI_MCP/
├── .venv/               # Virtual environment (Root)
├── modules/             # Resource-specific modules
│   ├── __init__.py
│   └── patient.py       # Patient resource tools
├── main.py              # Central MCP Server (Entry point)
├── requirements.txt      # Project dependencies
├── .env.template        # Configuration template
└── docs/                # Project documentation
```

## Setup

### 1. Create Virtual Environment

From the root directory of the project, run the command for your operating system:

**Windows:**
```powershell
python -m venv .venv
```

**macOS / Linux:**
```bash
python3 -m venv .venv
```

### 2. Activate Virtual Environment

**Windows (PowerShell):**
```powershell
.\.venv\Scripts\Activate.ps1
```

**Windows (Command Prompt):**
```cmd
.\.venv\Scripts\activate.bat
```

**macOS / Linux:**
```bash
source .venv/bin/activate
```

> [!NOTE]
> On Windows, the `source` command is not available. Use the direct path to the activation script instead.

### 3. Install Dependencies

Once the environment is active (you should see `(.venv)` in your terminal), install the required packages:

```bash
pip install -r requirements.txt
```

## Integration with LLMs

There are two main ways to connect this MCP server to an LLM like Claude or ChatGPT.

### 1. Claude Desktop (Standard - Stdio)
Claude Desktop expects to communicate with the server via standard input/output. You don't need a localhost URL for this; Claude will start the Python script as a background process.

**Configuration:**
Add this to your `claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "hapi-fhir": {
      "command": "C:\\Users\\Sayeed\\WorkSpace\\HAPI_MCP\\.venv\\Scripts\\python.exe",
      "args": ["C:\\Users\\Sayeed\\WorkSpace\\HAPI_MCP\\main.py"],
      "env": {
        "FHIR_BASE_URL": "https://fhir.datainterops.com/fhir"
      }
    }
  }
}
```

### 2. Remote / Web (SSE - HTTP)
If you want to access the server via a URL (e.g., if you are building a custom web app), you can run it in **SSE mode**.

**How to run in SSE mode:**
```bash
python main.py --transport sse
```
The server will be exposed at: `http://localhost:8000/sse`
**Important:** Use the full `/sse` path in your MCP client configuration.

### 3. Testing with MCP Inspector (GUI)
The inspector provides a graphical interface to test your tools.

**How to run:**
```bash
npx @modelcontextprotocol/inspector .venv\Scripts\python.exe main.py
```
After running this, open your browser to: `http://localhost:5173`

> [!TIP]
> **Port Summary:**
> - **8000**: Default port for the MCP Server in SSE mode.
> - **5173**: Default port for the MCP Inspector web UI.

## Security Note (Passthrough JWT)
This server **does not store** your credentials. Every request requires an `auth_token` provided by the LLM (which you must provide to the LLM during the session). This ensures that your HAPI FHIR server remains secure and only processes requests on your behalf.

## Deployment

This server can be deployed to various platforms.

### 1. Docker
You can build and run the server using Docker:

```bash
# Build the image
docker build -t hapi-mcp .

# Run the container (SSE mode)
docker run -p 8000:8000 -e FHIR_BASE_URL=https://fhir.datainterops.com/fhir hapi-mcp
```

### 2. PaaS (Render, Railway, etc.)
The project includes a `Procfile` for easy deployment to PaaS providers.

- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `python main.py --transport sse --host 0.0.0.0 --port $PORT`
- **Environment Variables:**
    - `FHIR_BASE_URL`: The base URL of your FHIR server.

### 3. Environment Variables
Ensure the following environment variables are set in your deployment environment:
| Variable | Description | Default |
|----------|-------------|---------|
| `FHIR_BASE_URL` | The base URL of the HAPI FHIR server | `https://fhir.datainterops.com/fhir` |
| `PORT` | The port for the SSE server (used by PaaS) | `8000` |
