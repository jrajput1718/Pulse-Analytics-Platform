# Pulse Analytics Platform

Pulse Analytics is a full-stack web analytics platform built with a Django REST API backend and a React dashboard frontend. It captures website traffic activity and visualizes page views, unique visitors, session duration, referrers, device types, browser mix, and geography.

## Project structure

- `backend/` contains the Django API and analytics data model.
- `frontend/` contains the React dashboard built with Vite.

## Backend setup

1. Create and activate a virtual environment.
2. Install dependencies:

   ```bash
   pip install -r backend/requirements.txt
   ```

3. Run database migrations:

   ```bash
   cd backend
   python manage.py migrate
   ```

4. Start the Django API:

   ```bash
   python manage.py runserver
   ```

The backend will be available at `http://127.0.0.1:8000/api`.

### API endpoints

- `POST /api/analytics/collect/`
- `GET /api/analytics/dashboard/?days=7`
- `GET /api/analytics/dashboard/?days=30&site=example.com`

### Example event payload

```json
{
  "event_type": "pageview",
  "site_domain": "example.com",
  "page_url": "https://example.com/pricing",
  "path": "/pricing",
  "page_title": "Pricing",
  "referrer": "https://google.com",
  "session_key": "session-123",
  "visitor_key": "visitor-abc",
  "device_type": "desktop",
  "browser": "Chrome",
  "os": "Windows",
  "country": "India",
  "region": "Karnataka",
  "city": "Bengaluru",
  "timezone": "Asia/Kolkata",
  "event_duration": 14
}
```

## Frontend setup

1. Install dependencies:

   ```bash
   cd frontend
   npm install
   ```

2. Start the React dashboard:

   ```bash
   npm run dev
   ```

3. If needed, create `frontend/.env` from `frontend/.env.example` and point `VITE_API_BASE_URL` at your Django API.

## Tracking flow

The dashboard includes an embeddable tracking snippet that:

- creates a persistent visitor ID with `localStorage`
- creates a per-tab session ID with `sessionStorage`
- sends a `pageview` event on load
- sends a `session_end` event on unload with the measured duration

## Notes for production

- Replace the Django secret key and analytics visitor salt.
- Add authentication and access control around the dashboard API.
- Use PostgreSQL for higher-volume environments.
- Enrich country, region, and city via a proxy or GeoIP service for fully automatic geographic reporting.
Screenshort:
<img width="975" height="548" alt="image" src="https://github.com/user-attachments/assets/e6119a70-8e1e-4531-80b8-06ec5b045d91" />
<img width="975" height="548" alt="image" src="https://github.com/user-attachments/assets/b0eeafa8-dccd-4027-b492-3307717da6aa" />
<img width="975" height="548" alt="image" src="https://github.com/user-attachments/assets/cbb104c8-86b4-4027-8f3e-4960d3b9eb95" />



