# modules/internet_metrics.py
from typing import Dict

import speedtest
from fastcli import fastcli


def get_internet_metrics() -> Dict[str, float]:
    """
    Get current internet speed and latency synchronously.

    Returns:
    - Dict[str, float]: Dictionary containing 'download_speed' (in Mbps),
                       'upload_speed' (in Mbps), and 'ping' (in milliseconds).
    """
    st = speedtest.Speedtest()
    st.get_best_server()

    # Get download speed in Mbps
    download_speed = st.download() / 1_000_000

    # Get upload speed in Mbps
    upload_speed = st.upload() / 1_000_000

    # Get ping in milliseconds
    ping = st.results.ping
    isp = st.results.client['isp']

    fast_download_speed = fastcli.run(timeout=2)

    return {
        'isp': isp,
        'download_speed': download_speed,
        'upload_speed': upload_speed,
        'ping': ping,
        'fast_download_speed': fast_download_speed
    }
