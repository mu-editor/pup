"""
PUP Plugin implementing the 'download' API.
"""

import hashlib
import logging

import httpx


_log = logging.getLogger(__name__)


class Step:

    """
    Downloads files from the given URL. Caches them to avoid future downloads.
    """

    @staticmethod
    def usable_in(ctx):
        return True


    def __call__(self, ctx, dsp, url):

        url_sha256 = hashlib.sha256(url.encode('utf8')).hexdigest()

        dirs = dsp.directories()
        cache_dir = dirs['cache']
        cached_download = cache_dir / url_sha256

        if cached_download.exists():
            return cached_download

        return self._download(url, dirname=cache_dir, filename=url_sha256)


    def _download(self, url, dirname, filename):

        if not dirname.exists():
            dirname.mkdir(parents=True)

        file = dirname / filename

        with open(file.with_suffix('.url'), 'wt', encoding='utf8') as f:
            f.write(url)

        _log.info(f'Downloading {url!r}...')
        with open(file, 'wb') as f, httpx.stream('GET', url, follow_redirects=True) as r:
            for chunk in r.iter_bytes():
                f.write(chunk)
        _log.info(f'Cached in {str(file)!r}.')

        return file
