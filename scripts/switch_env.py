import os
import sys
import shutil

# Configuration
BACKEND_ENV = "backend/.env"
FRONTEND_ENV = "src/.env" # Assuming Vite uses .env for local vs prod overrides sometimes

# Prod Constants (To be populated or prompted)
# Ideally these are NOT hardcoded but for this helper script we might need to know them
PROD_DB_URL = "postgresql://postgres:VvvOVxFbNDAhIDlyBTjZpykFXlwxxAdR@trolley.proxy.rlwy.net:11531/railway"
PROD_API_URL = "https://nielit-production.up.railway.app"

def set_local():
    print("🔄 Switching to LOCAL Mode...")
    
    # 1. Backend: SQLite
    with open(BACKEND_ENV, "w") as f:
        f.write("# Local Development (SQLite)\n")
        f.write("DATABASE_URL=sqlite:///./sql_app.db\n")
        f.write("PORT=8000\n")
    print(f"✅ Updated {BACKEND_ENV} -> SQLite")

    # 2. Frontend: Localhost
    # Note: We actually don't strictly need this because api.js defaults to localhost
    # But explicit is better for "Script Tracking"
    with open(FRONTEND_ENV, "w") as f:
        f.write("# Local Development\n")
        f.write("VITE_API_URL=http://localhost:8000\n")
    print(f"✅ Updated {FRONTEND_ENV} -> http://localhost:8000")
    
    print("\n🚀 Ready for LOCAL Development!")
    print("Run: cd backend && uvicorn app.main:app --reload")
    print("Run: npm run dev")

def set_prod():
    print("🔄 Switching to PRODUCTION Mode (Preparation)...")
    
    # 1. Backend: Postgres (For local debugging against Prod DB)
    with open(BACKEND_ENV, "w") as f:
        f.write("# Production Debugging (Railway DB)\n")
        f.write(f"DATABASE_URL={PROD_DB_URL}\n")
        f.write("PORT=8000\n")
    print(f"✅ Updated {BACKEND_ENV} -> Railway Postgres")

    # 2. Frontend: Prod URL
    # Useful if testing local frontend against Prod Backend
    with open(FRONTEND_ENV, "w") as f:
        f.write("# Production API\n")
        f.write(f"VITE_API_URL={PROD_API_URL}\n")
    print(f"✅ Updated {FRONTEND_ENV} -> {PROD_API_URL}")
    
    print("\n🚀 Ready for PRODUCTION Verification!")
    print("⚠️  WARNING: You are connected to the REAL Production Database.")

def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/switch_env.py [local|prod]")
        return

    mode = sys.argv[1].lower()
    
    if mode == "local":
        set_local()
    elif mode == "prod" or mode == "production":
        set_prod()
    else:
        print(f"Unknown mode: {mode}")

if __name__ == "__main__":
    main()
