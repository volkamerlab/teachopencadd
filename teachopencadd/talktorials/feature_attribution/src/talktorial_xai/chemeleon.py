import logging
from pathlib import Path

import torch
from chemprop import nn

from .paths import DATA

CHEMELEON_WEIGHTS = DATA / "models" / "chemelon_mp.pt"
CHEMELEON_URL = "https://zenodo.org/records/15460715/files/chemeleon_mp.pt"

logger = logging.getLogger(__name__)


def load_pretrained_chemeleon(
    weights: Path = CHEMELEON_WEIGHTS, download: bool = True
) -> nn.BondMessagePassing:
    if not weights.exists():
        if not download:
            raise FileNotFoundError(f"Chemeleon weights not found at {weights}")
        from urllib.request import urlretrieve

        weights.parent.mkdir(parents=True, exist_ok=True)
        logger.info("Downloading Chemeleon weights from Zenodo to %s", weights)
        urlretrieve(CHEMELEON_URL, str(weights))
    state = torch.load(weights, weights_only=True, map_location="cpu")
    message_passing = nn.BondMessagePassing(**state["hyper_parameters"])
    message_passing.load_state_dict(state["state_dict"])
    logger.info(
        "Loaded Chemeleon encoder (d_h=%d, depth=%d)",
        state["hyper_parameters"]["d_h"],
        state["hyper_parameters"]["depth"],
    )
    return message_passing
