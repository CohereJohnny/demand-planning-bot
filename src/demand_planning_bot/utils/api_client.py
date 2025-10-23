"""HTTP client utilities with error handling and retry logic.

Provides a robust HTTP client for external API integrations with:
- Comprehensive error handling
- Exponential backoff retry logic
- Rate limit detection
- Network timeout handling
"""

import logging
import time
from typing import Any, Dict, Optional

import httpx

logger = logging.getLogger(__name__)


class APIError(Exception):
    """Base exception for API-related errors."""

    pass


class RateLimitError(APIError):
    """Raised when API rate limit is exceeded."""

    pass


class APIClient:
    """HTTP client for external API requests with error handling."""

    def __init__(
        self,
        timeout: float = 30.0,
        max_retries: int = 3,
        retry_delay: float = 1.0,
    ):
        """Initialize the API client.

        Args:
            timeout: Request timeout in seconds.
            max_retries: Maximum number of retry attempts.
            retry_delay: Initial delay between retries in seconds (exponential backoff).
        """
        self.timeout = timeout
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.client = httpx.Client(timeout=timeout)

    def get(
        self,
        url: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        """Make a GET request with error handling and retries.

        Args:
            url: The URL to request.
            params: Query parameters.
            headers: HTTP headers.

        Returns:
            JSON response as a dictionary.

        Raises:
            APIError: For general API errors.
            RateLimitError: When rate limit is exceeded.
        """
        last_error: Optional[Exception] = None

        for attempt in range(self.max_retries):
            try:
                logger.debug(
                    f"Making GET request to {url} (attempt {attempt + 1}/{self.max_retries})"
                )

                response = self.client.get(url, params=params, headers=headers)

                # Handle rate limiting
                if response.status_code == 429:
                    retry_after = int(response.headers.get("Retry-After", "60"))
                    logger.warning(
                        f"Rate limit exceeded for {url}. Retry after {retry_after}s"
                    )
                    raise RateLimitError(
                        f"Rate limit exceeded. Retry after {retry_after} seconds"
                    )

                # Handle client errors (4xx)
                if 400 <= response.status_code < 500:
                    logger.error(
                        f"Client error {response.status_code} for {url}: {response.text}"
                    )
                    raise APIError(
                        f"Client error {response.status_code}: {response.text}"
                    )

                # Handle server errors (5xx)
                if response.status_code >= 500:
                    logger.warning(
                        f"Server error {response.status_code} for {url}. Will retry."
                    )
                    raise APIError(
                        f"Server error {response.status_code}: {response.text}"
                    )

                # Success!
                response.raise_for_status()
                logger.debug(f"Successfully received response from {url}")
                return response.json()

            except httpx.TimeoutException as e:
                logger.warning(f"Request timeout for {url} (attempt {attempt + 1})")
                last_error = e
                if attempt < self.max_retries - 1:
                    delay = self.retry_delay * (2**attempt)
                    logger.debug(f"Retrying after {delay}s...")
                    time.sleep(delay)

            except httpx.NetworkError as e:
                logger.warning(f"Network error for {url}: {e} (attempt {attempt + 1})")
                last_error = e
                if attempt < self.max_retries - 1:
                    delay = self.retry_delay * (2**attempt)
                    logger.debug(f"Retrying after {delay}s...")
                    time.sleep(delay)

            except RateLimitError:
                # Don't retry rate limit errors
                raise

            except APIError as e:
                if 500 <= e.args[0].split()[2] < 600:  # Server error
                    last_error = e
                    if attempt < self.max_retries - 1:
                        delay = self.retry_delay * (2**attempt)
                        logger.debug(f"Retrying after {delay}s...")
                        time.sleep(delay)
                else:
                    # Client errors shouldn't be retried
                    raise

        # All retries exhausted
        logger.error(f"All retry attempts exhausted for {url}")
        if last_error:
            raise APIError(
                f"Request failed after {self.max_retries} attempts"
            ) from last_error
        raise APIError(f"Request failed after {self.max_retries} attempts")

    def close(self) -> None:
        """Close the HTTP client."""
        self.client.close()

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
