"""Demo of non-hierarchical circuit simulations."""

from __future__ import annotations

import gdsfactory as gf
import jax.numpy as jnp
import sax


def straight(wl: float = 1.5, length: float = 10.0, neff: float = 2.4) -> sax.SDict:
    """Straight model."""
    return sax.reciprocal({("o1", "o2"): jnp.exp(2j * jnp.pi * neff * length / wl)})


def mmi1x2() -> sax.SDict:
    """Assumes a perfect 1x2 splitter."""
    return sax.reciprocal(
        {
            ("o1", "o2"): 0.5**0.5,
            ("o1", "o3"): 0.5**0.5,
        }
    )


def bend_euler(wl: float = 1.5, length: float = 20.0) -> sax.SDict:
    """Assumes reduced transmission for the euler bend compared to a straight."""
    return {k: 0.99 * v for k, v in straight(wl=wl, length=length).items()}


models = {
    "bend_euler": bend_euler,
    "mmi1x2": mmi1x2,
    "straight": straight,
}


def module(S: sax.SDict) -> None:
    for k, v in S.items():
        S[k] = jnp.abs(v) ** 2


if __name__ == "__main__":
    import matplotlib.pyplot as plt
    import numpy as np

    c = gf.components.mzi()
    c.show()
    netlist = c.get_netlist()
    circuit, _ = sax.circuit(netlist=netlist, models=models)
    wl = np.linspace(1.5, 1.6)
    S = circuit(wl=wl)

    plt.figure(figsize=(14, 4))
    plt.title("MZI")
    plt.plot(1e3 * wl, jnp.abs(S["o1", "o2"]) ** 2)
    plt.xlabel("λ [nm]")
    plt.ylabel("T")
    plt.grid(True)
    plt.show()
