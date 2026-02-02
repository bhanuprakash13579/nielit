# Project SAMARTH - Technical Deliverable

## 1. Overview
This repository contains the source code for the **State/District Inventory & Training Management System** (Project SAMARTH). It is designed to be 100% compliant with the RFP requirements for the ESDM Project.

## 2. Key Modules
*   **Inventory**: Asset tracking with hierarchical location and batch correlation (`src/pages/Inventory.jsx`).
*   **Training**: Batch management and NDU progress mapping (`src/pages/Training.jsx`).
*   **Content**: Digital asset metadata controller (`src/pages/Content.jsx`).
*   **Dashboard**: Executive Phase 1 tracking (`src/pages/Dashboard.jsx`).

## 3. Compliance Highlights
*   **Security**: Strict 2-Role System (Super Admin/Admin).
*   **Reporting**: Native PDF and Excel Exports.
*   **Audit**: Immutable `InventoryTransaction` ledger.
*   **Integration**: NDU Sync with Progress Logic.

### Deployment

#### Frontend (Vercel)
- **Repo:** `src/`
- **Build Command:** `npm run build`
- **Output Directory:** `dist`
- **IMPORTANT:** Do NOT set `VITE_API_URL` in Vercel.
  - The project uses a **Server-Side Proxy** (`vercel.json`) to route API requests to Railway.
  - This bypasses client-side DNS resolution issues (`ERR_NAME_NOT_RESOLVED`) common with some ISPs.
  - `src/utils/api.js` automatically detects Vercel and forces relative paths (`/api/v1/...`).

#### Backend (Railway)
- **Repo:** `backend/`
- **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- **Env Vars:**
  - `DATABASE_URL`: PostgreSQL Connection String
  - `PORT`: 8000

## 4. Setup
1.  `npm install`
2.  `cd backend && pip install -r requirements.txt`
3.  `npm run dev` (Frontend)
4.  `uvicorn app.main:app --reload` (Backend)

*Generated for Technical Bid Evaluation.*
