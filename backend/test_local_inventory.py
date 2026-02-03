import requests
import random

API_URL = "http://localhost:8000/api/v1"

def test_create_as_superadmin():
    # 1. Login
    print("Testing Login as superadmin...")
    try:
        res = requests.post(f"{API_URL}/auth/token", data={"username": "superadmin", "password": "password123"})
        if res.status_code != 200:
            print(f"❌ Login Failed: {res.text}")
            return
        token = res.json()["access_token"]
        print("✅ Login Successful")
    except Exception as e:
        print(f"❌ Connection Error: {e}")
        return

    # 2. Create Item
    kit_id = f"TEST-LOCAL-{random.randint(100,999)}"
    payload = {
        "kit_id": kit_id,
        "name": "Super Admin Test Item",
        "category": "Test",
        "status": "AVAILABLE",
        "quantity": 1,
        "state": "TestState",
        "district": "TestDistrict"
    }
    
    print(f"Attempting to create item as Super Admin: {kit_id}")
    res = requests.post(f"{API_URL}/inventory/", json=payload, headers={"Authorization": f"Bearer {token}"})
    
    if res.status_code == 200:
        print("✅ Success! Super Admin CAN create items.")
    else:
        print(f"❌ Failed: {res.status_code}")
        print(f"Response: {res.text}")

if __name__ == "__main__":
    test_create_as_superadmin()
