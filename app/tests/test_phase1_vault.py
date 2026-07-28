import pytest
import hashlib
from app.services.b2_service import b2_vault
from app.services.telemetry_service import telemetry_engine

def test_provenance_hash_generation():
    sample_bytes = b"NEXUS_SPATIAL_BINARY_TEST_DATA"
    prompt = "Test Cyberpunk Texture"
    seed = 123456
    
    expected_payload = sample_bytes + prompt.encode('utf-8') + str(seed).encode('utf-8')
    expected_hash = hashlib.sha256(expected_payload).hexdigest()
    
    calculated_hash = b2_vault.generate_provenance_hash(sample_bytes, prompt, seed)
    assert calculated_hash == expected_hash, "Provenance SHA256 mismatch!"

def test_telemetry_hmac_signature():
    raw_payload = b'{"test": "data"}'
    sig1 = telemetry_engine.generate_hmac_signature(raw_payload)
    sig2 = telemetry_engine.generate_hmac_signature(raw_payload)
    
    assert sig1 == sig2, "HMAC Signature must be deterministic!"
    assert len(sig1) == 64, "HMAC-SHA256 signature length must be 64 characters."

def test_presigned_url_generation():
    result = b2_vault.generate_presigned_direct_upload_slot("test_render.obj")
    assert "upload_endpoint" in result
    assert "authorization_token" in result
    assert result["expires_in_seconds"] == 3600
    assert "headers" in result