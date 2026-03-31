import os
import requests
import msal

def upload_to_sharepoint(file_path: str):
    """
    Uploads a file to a SharePoint Document Library via Microsoft Graph API.
    """
    tenant_id     = os.environ["AZURE_TENANT_ID"]
    client_id     = os.environ["AZURE_CLIENT_ID"]
    client_secret = os.environ["AZURE_CLIENT_SECRET"]
    sharepoint_site_id  = os.environ["SHAREPOINT_SITE_ID"]
    sharepoint_drive_id = os.environ["SHAREPOINT_DRIVE_ID"]
    sharepoint_folder   = os.environ["SHAREPOINT_FOLDER_PATH"]  # e.g. "HR Reports"

    # --- Authenticate via MSAL ---
    app = msal.ConfidentialClientApplication(
        client_id,
        authority=f"https://login.microsoftonline.com/{tenant_id}",
        client_credential=client_secret,
    )
    token_result = app.acquire_token_for_client(
        scopes=["https://graph.microsoft.com/.default"]
    )
    if "access_token" not in token_result:
        raise Exception(f"Auth failed: {token_result.get('error_description')}")

    access_token = token_result["access_token"]
    file_name    = os.path.basename(file_path)

    # --- Upload file ---
    upload_url = (
        f"https://graph.microsoft.com/v1.0/sites/{sharepoint_site_id}"
        f"/drives/{sharepoint_drive_id}/items/root:/"
        f"{sharepoint_folder}/{file_name}:/content"
    )

    with open(file_path, "rb") as f:
        response = requests.put(
            upload_url,
            headers={
                "Authorization": f"Bearer {access_token}",
                "Content-Type":  "application/octet-stream",
            },
            data=f,
        )

    response.raise_for_status()
    print(f"[uploader] Uploaded '{file_name}' to SharePoint successfully.")