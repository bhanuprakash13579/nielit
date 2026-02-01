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

## 4. Setup
1.  `npm install`
2.  `cd backend && pip install -r requirements.txt`
3.  `npm run dev` (Frontend)
4.  `uvicorn app.main:app --reload` (Backend)

*Generated for Technical Bid Evaluation.*
