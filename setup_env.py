import os
print("Please enter your GOOGLE_API_KEY:")
api_key = input().strip()
with open(".env", "w") as f:
    f.write(f"GOOGLE_API_KEY={api_key}\n")
print(".env file created.")
