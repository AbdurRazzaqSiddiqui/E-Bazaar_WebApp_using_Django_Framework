"""Django storage backend for public Vercel Blob product media."""

from __future__ import annotations

from io import BytesIO
import json
import mimetypes
import os
from pathlib import PurePosixPath
import time
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlencode
from urllib.request import Request, urlopen
from uuid import uuid4

from django.core.exceptions import ImproperlyConfigured
from django.core.files.base import File
from django.core.files.storage import Storage


class VercelBlobStorage(Storage):
    """Persist uploaded media in a public Vercel Blob store.

    Vercel currently exposes Blob's supported server-upload API through its
    official SDK. This backend speaks the same HTTP API so Django ImageFields
    can use the store without writing to a serverless function's local disk.
    """

    api_url = "https://vercel.com/api/blob"
    api_version = "12"
    max_upload_bytes = 4 * 1024 * 1024

    def __init__(self, token: str | None = None, store_id: str | None = None):
        self.token = token or os.getenv("BLOB_READ_WRITE_TOKEN", "")
        if not self.token:
            raise ImproperlyConfigured(
                "BLOB_READ_WRITE_TOKEN is required for Vercel Blob media storage."
            )
        self.store_id = (store_id or os.getenv("BLOB_STORE_ID", "")).removeprefix(
            "store_"
        )
        if not self.store_id:
            parts = self.token.split("_")
            self.store_id = parts[3] if len(parts) > 3 else ""
        if not self.store_id:
            raise ImproperlyConfigured("Unable to determine the Vercel Blob store ID.")

    @property
    def public_base_url(self) -> str:
        return f"https://{self.store_id}.public.blob.vercel-storage.com"

    def get_available_name(self, name, max_length=None):
        path = PurePosixPath(str(name).replace("\\", "/"))
        suffix = path.suffix.lower()
        unique_suffix = f"-{uuid4().hex[:12]}"
        stem = path.stem
        parent = "" if str(path.parent) == "." else f"{path.parent}/"
        if max_length:
            available = max_length - len(parent) - len(unique_suffix) - len(suffix)
            stem = stem[: max(1, available)]
        return f"{parent}{stem}{unique_suffix}{suffix}"

    def _headers(self, attempt=0, **extra):
        headers = {
            "Authorization": f"Bearer {self.token}",
            "x-vercel-blob-store-id": self.store_id,
            "x-api-version": os.getenv("VERCEL_BLOB_API_VERSION_OVERRIDE", self.api_version),
            "x-api-blob-request-id": f"{self.store_id}:{int(time.time() * 1000)}:{uuid4().hex}",
            "x-api-blob-request-attempt": str(attempt),
        }
        headers.update(extra)
        return headers

    def _request(self, path, *, method="GET", body=None, headers=None):
        last_error = None
        for attempt in range(3):
            request = Request(
                f"{self.api_url}{path}",
                data=body,
                method=method,
                headers=self._headers(attempt, **(headers or {})),
            )
            try:
                with urlopen(request, timeout=30) as response:
                    payload = response.read()
                    return json.loads(payload) if payload else {}
            except HTTPError as exc:
                last_error = exc
                if exc.code < 500 or attempt == 2:
                    detail = exc.read().decode("utf-8", errors="replace")
                    raise OSError(f"Vercel Blob request failed ({exc.code}): {detail}") from exc
            except URLError as exc:
                last_error = exc
                if attempt == 2:
                    break
            time.sleep(0.2 * (2**attempt))
        raise OSError("Vercel Blob request failed after retries.") from last_error

    def _save(self, name, content):
        body = b"".join(content.chunks())
        if len(body) > self.max_upload_bytes:
            raise ValueError("Product images uploaded through Vercel must be 4 MB or smaller.")
        content_type = getattr(content, "content_type", None)
        content_type = content_type or mimetypes.guess_type(name)[0] or "application/octet-stream"
        response = self._request(
            f"/?{urlencode({'pathname': name})}",
            method="PUT",
            body=body,
            headers={
                "x-vercel-blob-access": "public",
                "x-add-random-suffix": "0",
                "x-allow-overwrite": "0",
                "x-content-type": content_type,
            },
        )
        return response["pathname"]

    def _open(self, name, mode="rb"):
        if "b" not in mode:
            raise ValueError("Vercel Blob media files must be opened in binary mode.")
        with urlopen(self.url(name), timeout=30) as response:
            return File(BytesIO(response.read()), name=name)

    def delete(self, name):
        if not name:
            return
        body = json.dumps({"urls": [self.url(name)]}).encode("utf-8")
        self._request(
            "/delete",
            method="POST",
            body=body,
            headers={"Content-Type": "application/json"},
        )

    def exists(self, name):
        # Names include a random suffix before upload, so collisions are not possible.
        return False

    def size(self, name):
        request = Request(self.url(name), method="HEAD")
        with urlopen(request, timeout=30) as response:
            return int(response.headers.get("Content-Length", "0"))

    def url(self, name):
        if str(name).startswith(("http://", "https://")):
            return str(name)
        return f"{self.public_base_url}/{quote(str(name), safe='/')}"
