import uuid
import json
import hashlib
from typing import Dict, Any, Optional
from b2sdk.v2 import B2Api, InMemoryAccountInfo
from app.core.config import settings


class B2VaultService:
    def __init__(self):
        self.info = InMemoryAccountInfo()
        self.b2_api = B2Api(self.info)
        
        try:
            self.account_info = self.b2_api.authorize_account(
                "production", 
                settings.B2_KEY_ID, 
                settings.B2_APPLICATION_KEY
            )
            self.bucket = self.b2_api.get_bucket_by_name(settings.B2_BUCKET_NAME)
            self._validate_b2_capabilities()
        except Exception as e:
            raise RuntimeError(f"B2 Vault Boot Failure: {str(e)}")

    def _validate_b2_capabilities(self):
        """Pre-flight Gatekeeper: Verifies Application Key permissions at startup."""
        allowed_capabilities = self.info.get_allowed()
        required = ["writeFiles", "readFiles", "listFiles"]
        capabilities = allowed_capabilities.get("capabilities", [])
        
        if "*" not in capabilities:
            missing = [cap for cap in required if cap not in capabilities]
            if missing:
                raise PermissionError(f"CRITICAL: B2 Application Key missing required capabilities: {missing}")

    def _sanitize_metadata_value(self, value: str, max_len: int = 240) -> str:
        """Ensures metadata strings are ASCII-safe and within HTTP header limits."""
        cleaned = value.encode("ascii", "ignore").decode("ascii")
        return cleaned[:max_len]

    def generate_provenance_hash(self, file_bytes: bytes, prompt: str, seed: int) -> str:
        """Calculates SHA-256 fingerprint linking binary payload, prompt, and seed."""
        payload = file_bytes + prompt.encode('utf-8') + str(seed).encode('utf-8')
        return hashlib.sha256(payload).hexdigest()

    def upload_asset_with_provenance(
        self, 
        file_bytes: bytes, 
        file_name: str, 
        content_type: str, 
        prompt: str, 
        seed: int, 
        parent_id: str = "root",
        provider_info: str = "Genblaze-Core",
        fallback_triggered: bool = False
    ) -> Dict[str, Any]:
        """
        Vaults binary assets into Backblaze B2 and attaches header-safe metadata.
        """
        version_commit_id = f"commit-{uuid.uuid4().hex[:10]}"
        provenance_hash = self.generate_provenance_hash(file_bytes, prompt, seed)
        
        # Clean metadata key names and values (b2sdk maps these to X-Bz-Info-* headers)
        custom_metadata = {
            "Prompt": self._sanitize_metadata_value(prompt, 240),
            "Seed": str(seed),
            "Version-ID": version_commit_id,
            "Parent-Node": self._sanitize_metadata_value(parent_id, 100),
            "Provenance-Hash": provenance_hash,
            "AI-Provider": self._sanitize_metadata_value(provider_info, 100),
            "Fallback-Triggered": str(fallback_triggered),
            "Engine-Signature": "AETHER-MIND-NEXUS-v5"
        }

        file_info = self.bucket.upload_bytes(
            data_bytes=file_bytes,
            file_name=f"spatial_vault/{version_commit_id}/{file_name}",
            content_type=content_type,
            file_infos=custom_metadata
        )

        durable_url = self.b2_api.get_download_url_for_file_name(
            bucket_name=settings.B2_BUCKET_NAME,
            file_name=file_info.file_name
        )

        return {
            "file_id": file_info.id_,
            "file_name": file_info.file_name,
            "version_commit_id": version_commit_id,
            "provenance_hash": provenance_hash,
            "durable_url": durable_url,
            "metadata": custom_metadata
        }

    def generate_presigned_direct_upload_slot(self, file_name: str, valid_duration_sec: int = 3600) -> Dict[str, Any]:
        """Generates direct Backblaze B2 upload endpoint and auth token for client streaming."""
        file_path = f"direct_ingest/{uuid.uuid4().hex[:8]}_{file_name}"
        
        upload_url_data = self.b2_api.session.get_upload_url(self.bucket.id_)
        upload_endpoint = upload_url_data['uploadUrl']
        auth_token = upload_url_data['authorizationToken']

        return {
            "target_file_path": file_path,
            "upload_endpoint": upload_endpoint,
            "authorization_token": auth_token,
            "expires_in_seconds": valid_duration_sec,
            "headers": {
                "Authorization": auth_token,
                "X-Bz-File-Name": file_path,
                "Content-Type": "b2/x-auto"
            },
            "instructions": "POST binary content directly to 'upload_endpoint' with provided headers."
        }

    def vault_telemetry_audit_ledger(self, telemetry_payload: Dict[str, Any]) -> str:
        """Vaults immutable execution metrics directly into Backblaze B2."""
        commit_id = telemetry_payload["associated_commit_id"]
        telemetry_id = telemetry_payload["telemetry_id"]
        json_bytes = json.dumps(telemetry_payload, indent=2).encode('utf-8')

        file_info = self.bucket.upload_bytes(
            data_bytes=json_bytes,
            file_name=f"telemetry_vault/{commit_id}_{telemetry_id}.json",
            content_type="application/json",
            file_infos={
                "Type": "telemetry_audit_snapshot",
                "HMAC-Sig": self._sanitize_metadata_value(
                    telemetry_payload.get("cryptographic_signature", ""), 128
                )
            }
        )
        return self.b2_api.get_download_url_for_file_name(
            bucket_name=settings.B2_BUCKET_NAME,
            file_name=file_info.file_name
        )

    def upload_version_manifest(self, manifest_data: Dict[str, Any]) -> str:
        """Vaults immutable Graph Ledger Node manifests into Backblaze B2."""
        commit_id = manifest_data["version_commit_id"]
        json_bytes = json.dumps(manifest_data, indent=2).encode('utf-8')
        
        file_info = self.bucket.upload_bytes(
            data_bytes=json_bytes,
            file_name=f"manifest_ledger/{commit_id}_manifest.json",
            content_type="application/json",
            file_infos={"Type": "provenance_manifest_ledger"}
        )
        return file_info.id_


# --- SAFE RESILIENT SINGLETON INITIALIZATION ---
_b2_vault_instance: Optional[B2VaultService] = None

def get_b2_vault() -> Optional[B2VaultService]:
    """Lazy Loader: Safe instance retriever preventing startup crashes."""
    global _b2_vault_instance
    if _b2_vault_instance is None:
        try:
            _b2_vault_instance = B2VaultService()
        except Exception as e:
            print(f"⚠️ Warning: B2 Vault initialization deferred/failed: {e}")
            return None
    return _b2_vault_instance

# Global Safe Instance for direct imports
try:
    b2_vault = B2VaultService()
except Exception as e:
    print(f"⚠️ Warning: B2 Vault startup bypassed to keep server running: {e}")
    b2_vault = None

# Backward-compatibility aliases
B2VaultServiceDay4 = B2VaultService
B2VaultServiceDay5 = B2VaultService