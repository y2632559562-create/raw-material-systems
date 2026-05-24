# Streamlit App

A Python Streamlit web application with interactive charts, data tables, and form components.

## Run & Operate

- `cd streamlit-app && streamlit run app.py --server.port 5000` — run the Streamlit app
- Workflow: "Start application" (auto-starts on port 5000)

## Stack

- Python 3.11
- Streamlit
- Pandas, NumPy

## Where things live

- `streamlit-app/app.py` — main application entry point
- `streamlit-app/.streamlit/config.toml` — Streamlit server config (headless, port 5000)
- `streamlit-app/requirements.txt` — Python dependencies

## Architecture decisions

- Single-file Streamlit app for simplicity — add pages via `streamlit-app/pages/` directory as the app grows
- Server config locks port to 5000 and disables CORS/XSRF for the Replit environment

## Product

A starter Streamlit app with an interactive line/bar/area chart, a sample data table, and a simple form — ready to be extended with real data and logic.

## User preferences

_Populate as you build — explicit user instructions worth remembering across sessions._

## Gotchas

- Always run from within the `streamlit-app/` directory so `.streamlit/config.toml` is picked up automatically
- Do not change `.streamlit/config.toml` server settings — they are tuned for the Replit proxy environment

## Pointers

- See the `pnpm-workspace` skill for workspace structure, TypeScript setup, and package details
