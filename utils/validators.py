from urllib.parse import urlparse
import socket
import requests
from typing import Tuple
import re


def is_valid_url(url: str) -> Tuple[bool, str]:
    try:
        result = urlparse(url)
        if not all([result.scheme, result.netloc]):
            return False, "Invalid URL format"

        if result.scheme not in ["http", "https"]:
            return False, "URL must start with http:// or https://"

        domain_pattern = (
            r"^([a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$"
        )
        if not re.match(domain_pattern, result.netloc):
            return False, "Invalid domain format"

        try:
            socket.gethostbyname(result.netloc)
        except socket.gaierror:
            return False, "Unable to resolve domain"

        try:
            response = requests.head(url, timeout=5, allow_redirects=True)
            if response.status_code >= 400:
                return False, f"URL returned error status {response.status_code}"
            return True, ""
        except requests.exceptions.SSLError:
            return False, "SSL certificate verification failed"
        except requests.exceptions.ConnectionError:
            return False, "Failed to establish connection"
        except requests.exceptions.Timeout:
            return False, "Connection timed out"
        except requests.exceptions.RequestException:
            return False, "Failed to validate URL"

    except Exception as e:
        return False, f"Invalid URL: {str(e)}"
