from typing import Dict, Any
from fastapi import APIRouter

router = APIRouter(prefix="/pwa", tags=["PWA"])

class PWAManifestBuilder:
    """Generates customized PWA manifests depending on the user's role profile."""
    @staticmethod
    def build_manifest(role: str) -> Dict[str, Any]:
        base_manifest = {
            "short_name": "CleanConnect",
            "name": "Clean Connect - Swachh Bharat",
            "icons": [
                {
                    "src": "/assets/icon-192.png",
                    "type": "image/png",
                    "sizes": "192x192"
                }
            ],
            "display": "standalone",
            "orientation": "portrait",
            "theme_color": "#1F8A70"
        }

        if role == "CITIZEN":
            base_manifest.update({
                "start_url": "/pwa/citizen/dashboard",
                "name": "Clean Connect: Citizen Reporting App",
                "description": "Report local garbage piles, track smart bins, and view municipal actions."
            })
        elif role == "WORKER":
            base_manifest.update({
                "start_url": "/pwa/worker/dashboard",
                "name": "Clean Connect: Sanitation Crew App",
                "description": "Receive assigned cleanup operations and navigate directly to target coordinates."
            })
        else:
            base_manifest.update({
                "start_url": "/admin/dashboard",
                "name": "Clean Connect: Central Command Admin Portal",
                "description": "Monitor urban sanitation metrics and audit active worker metrics."
            })
        return base_manifest

@router.get("/manifest.json")
def get_pwa_manifest(role: str = "CITIZEN"):
    """Serves distinct, role-scoped manifests for targeted PWA installation."""
    role_clean = role.upper()
    return PWAManifestBuilder.build_manifest(role_clean)
