#!/usr/bin/env python3
"""
Simple test script to demonstrate the Feature Flag API functionality.
Run this after starting the API server.
"""

import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

def test_api():
    print("🚀 Testing Feature Flag API...\n")
    
    # 1. Create an admin user
    print("1. Creating admin user...")
    signup_data = {
        "email": "admin@example.com",
        "username": "admin",
        "password": "password123",
        "role": "admin"
    }
    
    response = requests.post(f"{BASE_URL}/auth/signup", json=signup_data)
    if response.status_code == 200:
        print("✅ Admin user created successfully")
        user_data = response.json()
        print(f"   User ID: {user_data['id']}")
    else:
        print(f"❌ Failed to create admin user: {response.text}")
        return
    
    # 2. Login and get token
    print("\n2. Logging in...")
    login_data = {
        "username": "admin",
        "password": "password123"
    }
    
    response = requests.post(f"{BASE_URL}/auth/token", data=login_data)
    if response.status_code == 200:
        token_data = response.json()
        token = token_data["access_token"]
        print("✅ Login successful")
        print(f"   Token: {token[:20]}...")
    else:
        print(f"❌ Login failed: {response.text}")
        return
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # 3. Create a project
    print("\n3. Creating a project...")
    project_data = {
        "name": "Test Web App",
        "description": "A test web application for feature flags"
    }
    
    response = requests.post(f"{BASE_URL}/projects/", json=project_data, headers=headers)
    if response.status_code == 200:
        project = response.json()
        project_id = project["id"]
        print("✅ Project created successfully")
        print(f"   Project ID: {project_id}")
        print(f"   Project Name: {project['name']}")
    else:
        print(f"❌ Failed to create project: {response.text}")
        return
    
    # 4. Create a feature flag
    print("\n4. Creating a feature flag...")
    flag_data = {
        "name": "new_ui_feature",
        "description": "Enable the new user interface",
        "is_enabled": True,
        "environment": "dev",
        "project_id": project_id,
        "user_group_targeting": '{"groups": ["beta_users", "early_adopters"]}'
    }
    
    response = requests.post(f"{BASE_URL}/feature-flags/", json=flag_data, headers=headers)
    if response.status_code == 200:
        flag = response.json()
        flag_id = flag["id"]
        print("✅ Feature flag created successfully")
        print(f"   Flag ID: {flag_id}")
        print(f"   Flag Name: {flag['name']}")
        print(f"   Enabled: {flag['is_enabled']}")
        print(f"   Environment: {flag['environment']}")
    else:
        print(f"❌ Failed to create feature flag: {response.text}")
        return
    
    # 5. List feature flags
    print("\n5. Listing feature flags...")
    response = requests.get(f"{BASE_URL}/feature-flags/?project_id={project_id}", headers=headers)
    if response.status_code == 200:
        flags = response.json()
        print(f"✅ Found {len(flags)} feature flag(s)")
        for flag in flags:
            print(f"   - {flag['name']}: {flag['description']} ({flag['environment']})")
    else:
        print(f"❌ Failed to list feature flags: {response.text}")
    
    # 6. Update feature flag
    print("\n6. Updating feature flag...")
    update_data = {
        "is_enabled": False,
        "description": "Enable the new user interface (disabled for testing)"
    }
    
    response = requests.put(f"{BASE_URL}/feature-flags/{flag_id}", json=update_data, headers=headers)
    if response.status_code == 200:
        updated_flag = response.json()
        print("✅ Feature flag updated successfully")
        print(f"   Enabled: {updated_flag['is_enabled']}")
        print(f"   Description: {updated_flag['description']}")
    else:
        print(f"❌ Failed to update feature flag: {response.text}")
    
    # 7. Get current user info
    print("\n7. Getting current user info...")
    response = requests.get(f"{BASE_URL}/auth/me", headers=headers)
    if response.status_code == 200:
        user = response.json()
        print("✅ User info retrieved")
        print(f"   Username: {user['username']}")
        print(f"   Email: {user['email']}")
        print(f"   Role: {user['role']}")
    else:
        print(f"❌ Failed to get user info: {response.text}")
    
    print("\n🎉 API test completed successfully!")
    print(f"\n📚 API Documentation: http://localhost:8000/docs")
    print(f"🔗 ReDoc: http://localhost:8000/redoc")

if __name__ == "__main__":
    try:
        test_api()
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to the API server.")
        print("   Make sure the server is running on http://localhost:8000")
        print("   Run: uvicorn app.main:app --reload")
    except Exception as e:
        print(f"❌ An error occurred: {e}") 