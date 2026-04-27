import base64
import time
from typing import Dict, List, Optional
from urllib.parse import urlencode

import requests


class SpotifyClient:
    AUTH_URL = "https://accounts.spotify.com/authorize"
    TOKEN_URL = "https://accounts.spotify.com/api/token"
    API_BASE = "https://api.spotify.com/v1"

    SCOPES = " ".join([
        "user-read-playback-state",
        "user-modify-playback-state",
        "user-read-currently-playing",
        "user-library-read",
    ])

    def __init__(self, client_id: str, client_secret: str, redirect_uri: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self._access_token: Optional[str] = None
        self._refresh_token: Optional[str] = None
        self._expires_at: float = 0.0


    def get_auth_url(self, state: str) -> str:
        params = {
            "client_id": self.client_id,
            "response_type": "code",
            "redirect_uri": self.redirect_uri,
            "scope": self.SCOPES,
            "state": state,
        }
        return f"{self.AUTH_URL}?{urlencode(params)}"

    def exchange_code(self, code: str) -> bool:
        resp = requests.post(
            self.TOKEN_URL,
            headers=self._basic_auth_header(),
            data={
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": self.redirect_uri,
            },
        )
        if resp.status_code == 200:
            self._save_tokens(resp.json())
            return True
        return False

    def is_authenticated(self) -> bool:
        return bool(self._access_token or self._refresh_token)

    def logout(self):
        self._access_token = None
        self._refresh_token = None
        self._expires_at = 0.0

    def _save_tokens(self, data: Dict):
        self._access_token = data["access_token"]
        if "refresh_token" in data:
            self._refresh_token = data["refresh_token"]
        # Subtract 60 s buffer so we refresh before true expiry
        self._expires_at = time.time() + data["expires_in"] - 60

    def _basic_auth_header(self) -> Dict[str, str]:
        encoded = base64.b64encode(
            f"{self.client_id}:{self.client_secret}".encode()
        ).decode()
        return {
            "Authorization": f"Basic {encoded}",
            "Content-Type": "application/x-www-form-urlencoded",
        }

    def _refresh_access_token(self) -> bool:
        if not self._refresh_token:
            return False
        resp = requests.post(
            self.TOKEN_URL,
            headers=self._basic_auth_header(),
            data={
                "grant_type": "refresh_token",
                "refresh_token": self._refresh_token,
            },
        )
        if resp.status_code == 200:
            self._save_tokens(resp.json())
            return True
        return False

    def _ensure_token(self) -> bool:
        if not self.is_authenticated():
            return False
        if time.time() >= self._expires_at:
            return self._refresh_access_token()
        return True

    def _request(self, method: str, path: str, **kwargs) -> Optional[requests.Response]:
        if not self._ensure_token():
            return None

        headers = kwargs.pop("headers", {})
        headers["Authorization"] = f"Bearer {self._access_token}"

        delay = 1
        for _ in range(3):
            resp = requests.request(
                method,
                f"{self.API_BASE}{path}",
                headers=headers,
                **kwargs,
            )
            if resp.status_code == 429:
                wait = int(resp.headers.get("Retry-After", delay))
                time.sleep(wait)
                delay = min(delay * 2, 30)
                continue
            return resp

        return None

    def get_current_playback(self) -> Optional[Dict]:
        resp = self._request("GET", "/me/player")
        if resp is None:
            return None
        if resp.status_code == 200:
            return resp.json()
        if resp.status_code == 204:
            return {}  # session active but nothing playing
        return None

    def play(self) -> bool:
        resp = self._request("PUT", "/me/player/play")
        return resp is not None and resp.status_code in (200, 204)

    def pause(self) -> bool:
        resp = self._request("PUT", "/me/player/pause")
        return resp is not None and resp.status_code in (200, 204)

    def skip_next(self) -> bool:
        resp = self._request("POST", "/me/player/next")
        return resp is not None and resp.status_code == 204

    def skip_previous(self) -> bool:
        resp = self._request("POST", "/me/player/previous")
        return resp is not None and resp.status_code == 204

    def search_track(self, title: str, artist: str) -> Optional[Dict]:
        resp = self._request(
            "GET",
            "/search",
            params={
                "q": f"track:{title} artist:{artist}",
                "type": "track",
                "limit": 1,
            },
        )
        if resp and resp.status_code == 200:
            items = resp.json().get("tracks", {}).get("items", [])
            return items[0] if items else None
        return None

    def get_album_art_url(self, title: str, artist: str) -> Optional[str]:
        track = self.search_track(title, artist)
        if not track:
            return None
        images: List[Dict] = track.get("album", {}).get("images", [])
        return images[0]["url"] if images else None

    # ── User library ──────────────────────────────────────────────────────────

    def get_saved_tracks(self, limit: int = 50) -> List[Dict]:
        """Return up to `limit` of the user's liked tracks.

        Returns an empty list if the token lacks user-library-read scope (403).
        """
        tracks: List[Dict] = []
        offset = 0
        while len(tracks) < limit:
            batch = min(50, limit - len(tracks))
            resp = self._request(
                "GET", "/me/tracks", params={"limit": batch, "offset": offset}
            )
            if resp is None or resp.status_code == 403:
                break
            if resp.status_code != 200:
                break
            data = resp.json()
            items = data.get("items", [])
            if not items:
                break
            tracks.extend(item["track"] for item in items if item.get("track"))
            if not data.get("next"):
                break
            offset += batch
        return tracks

    def get_artists(self, artist_ids: List[str]) -> List[Dict]:
        """Batch-fetch artist objects (max 50 per request) to get genre tags."""
        results: List[Dict] = []
        for i in range(0, len(artist_ids), 50):
            batch = artist_ids[i : i + 50]
            resp = self._request(
                "GET", "/artists", params={"ids": ",".join(batch)}
            )
            if resp and resp.status_code == 200:
                results.extend(resp.json().get("artists", []))
        return results
