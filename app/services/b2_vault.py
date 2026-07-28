import io
import hashlib
from typing import Dict, Any, Optional
from b2sdk.v2 import B2Api, InMemoryAccountInfo
from app.core.config import settings

class B2VaultManager:
    """
    High-performance B2 Vault Manager with deterministic 
    lineage tracking via custom object metadata.
    """
    def __init__(self):
        self.info = InMemoryAccountInfo()
        self.b2_api = B2Api(self.info)
        self._authenticated = False
        self.bucket = None

    def authenticate(self):
        if not self._authenticated:
            self.b2_api.authorize_account(
                "production", 
                settings.B2_KEY_ID, 
                settings.B2_APPLICATION_KEY
            )
            self.bucket = self.b2_api.get_bucket_by_name(settings.B2_BUCKET_NAME)
            self._authenticated = True

    def upload_artifact_with_lineage(
        self,
        file_bytes: bytes,
        filename: str,
        prompt_text: str,
        seed: int,
        version_commit_id: str,
        parent_commit_id: Optional[str] = None
    ) -> Dict[str, Any]:
        self.authenticate()

        # Strict B2 Custom Metadata Tagging
        custom_metadata = {
            "Prompt": prompt_text,
            "Seed": str(seed),
            "Version": version_commit_id,
            "Parent-Node": parent_commit_id if parent_commit_id else "ROOT"
        }

        # Compatible upload_bytes call without unsupported keyword arguments
        file_info = self.bucket.upload_bytes(
            data_bytes=file_bytes,
            file_name=filename,
            content_type="application/octet-stream",
            file_infos=custom_metadata
        )

        return {
            "file_id": file_info.id_,
            "file_name": file_info.file_name,
            "version_commit_id": version_commit_id,
            "parent_commit_id": parent_commit_id or "ROOT",
            "metadata_attached": custom_metadata
        }

b2_vault = B2VaultManager()