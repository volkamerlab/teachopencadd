from __future__ import annotations

import io
from collections.abc import Sequence

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import colormaps
from matplotlib.cm import ScalarMappable
from matplotlib.colors import Colormap, ListedColormap, Normalize
from mpl_toolkits.axes_grid1 import make_axes_locatable
from PIL import Image
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem.Draw import SimilarityMaps, rdMolDraw2D

from talktorial_xai.attribution import MolAttribution

__all__ = [
    "ATTRIBUTION_CMAP",
    "draw_atom_attributions",
    "draw_attribution_panel",
    "draw_bit_attributions",
    "draw_molecule",
    "prepare_mol",
    "save",
    "trim_colormap",
]


def trim_colormap(
    cmap: str | Colormap = "RdBu_r",
    trim: float = 0.12,
    n: int = 256,
) -> Colormap:
    """A diverging colormap with its darkest extremes cut off.

    ColorBrewer's diverging maps run to near-black at both ends (RdBu's
    ends sit at CIE L* 20), which is fine for a heatmap but not for filling
    atom highlights: a strongly attributed nitrogen turns into a dark blob
    with its element label swallowed. Dropping the outer ``trim`` of the
    ramp keeps the hues and the white neutral point, and lifts the ends to
    roughly L* 40 -- still clearly the extreme, still readable through.

    The scale stays symmetric, so equal magnitudes keep equal weight.

    Parameters
    ----------
    trim
        Fraction cut from each end. 0.12 is the default; 0.2 is noticeably
        pastel, above that the extremes stop reading as extreme.
    """
    if not 0.0 <= trim < 0.5:
        raise ValueError(f"trim must be in [0, 0.5), got {trim}")
    base = colormaps[cmap] if isinstance(cmap, str) else cmap
    name = f"{getattr(base, 'name', 'cmap')}_trim{trim:g}"
    return ListedColormap(base(np.linspace(trim, 1.0 - trim, n)), name=name)


#: Default scale for every attribution figure in this talktorial: RdBu_r
#: with the near-black ends trimmed away.
ATTRIBUTION_CMAP = trim_colormap("RdBu_r", 0.12)


# --------------------------------------------------------------------------
# helpers
# --------------------------------------------------------------------------


def prepare_mol(smiles_or_mol, add_hs: bool = False) -> Chem.Mol:
    """Return a molecule with sane 2D coordinates for drawing."""
    if isinstance(smiles_or_mol, str):
        mol = Chem.MolFromSmiles(smiles_or_mol)
        if mol is None:
            raise ValueError(f"could not parse SMILES: {smiles_or_mol!r}")
    else:
        mol = Chem.Mol(smiles_or_mol)

    if add_hs:
        mol = Chem.AddHs(mol)

    if mol.GetNumConformers() == 0:
        AllChem.Compute2DCoords(mol)
    return mol


def _symmetric_norm(weights: np.ndarray, vmax: float | None) -> Normalize:
    """Diverging scale centred on zero.

    Centring on zero is not cosmetic: an attribution scale whose midpoint
    drifts with the data makes 'this group pushes the prediction up' and
    'this group is merely less negative than its neighbours' look the same.
    """
    if vmax is None:
        vmax = float(np.max(np.abs(weights))) or 1.0
    return Normalize(vmin=-vmax, vmax=vmax)


def _png_to_array(
    png_bytes: bytes,
    background: str = "white",
    crop: bool = True,
    pad: int = 8,
) -> np.ndarray:
    img = np.array(Image.open(io.BytesIO(png_bytes)).convert("RGBA"))

    if background == "transparent":
        # RDKit's contour renderer paints opaque white regardless of
        # clearBackground, so knock pure white back out to alpha 0.
        pure_white = np.all(img[..., :3] == 255, axis=-1)
        img[pure_white, 3] = 0
    elif background == "white":
        # composite whatever transparency exists onto solid white, so the
        # saved PNG has no grey/checkerboard behind the structure
        a = img[..., 3:4].astype(float) / 255.0
        img[..., :3] = (img[..., :3] * a + 255 * (1 - a)).astype(np.uint8)
        img[..., 3] = 255
    else:
        raise ValueError("background must be 'white' or 'transparent'")

    if not crop:
        return img
    # blank = fully transparent, or opaque white
    alpha = img[..., 3]
    rgb = img[..., :3]
    blank = (alpha == 0) | ((alpha == 255) & np.all(rgb >= 250, axis=-1))
    rows = np.where(~blank.all(axis=1))[0]
    cols = np.where(~blank.all(axis=0))[0]
    if rows.size == 0 or cols.size == 0:
        return img
    r0, r1 = max(rows[0] - pad, 0), min(rows[-1] + pad + 1, img.shape[0])
    c0, c1 = max(cols[0] - pad, 0), min(cols[-1] + pad + 1, img.shape[1])
    return img[r0:r1, c0:c1]


def _render_atoms(
    mol: Chem.Mol,
    weights: np.ndarray,
    bond_weights: np.ndarray | None,
    norm: Normalize,
    cmap: Colormap,
    size: tuple[int, int],
    label_indices: bool,
    highlight_radius: float,
    background: str,
    alpha: float,
) -> bytes:
    """Discrete per-atom colouring.

    Bonds are coloured by their own attribution when one is given, and
    otherwise by the mean of their endpoints -- interpolation, not data.
    """
    atom_colors = {i: tuple(cmap(norm(w))[:3]) + (alpha,) for i, w in enumerate(weights)}
    bond_colors, bond_ids = {}, []
    for bond in mol.GetBonds():
        idx = bond.GetIdx()
        if bond_weights is None:
            w = 0.5 * (weights[bond.GetBeginAtomIdx()] + weights[bond.GetEndAtomIdx()])
        else:
            w = bond_weights[idx]
        bond_ids.append(idx)
        bond_colors[idx] = tuple(cmap(norm(w))[:3]) + (alpha,)

    drawer = rdMolDraw2D.MolDraw2DCairo(*size)
    opts = drawer.drawOptions()
    opts.clearBackground = True
    opts.setBackgroundColour((1, 1, 1, 0 if background == "transparent" else 1))
    opts.fillHighlights = True
    opts.highlightRadius = highlight_radius
    opts.highlightBondWidthMultiplier = 16
    opts.addAtomIndices = label_indices
    opts.bondLineWidth = 2

    rdMolDraw2D.PrepareAndDrawMolecule(
        drawer,
        mol,
        highlightAtoms=list(range(mol.GetNumAtoms())),
        highlightAtomColors=atom_colors,
        highlightBonds=bond_ids,
        highlightBondColors=bond_colors,
    )
    drawer.FinishDrawing()
    return drawer.GetDrawingText()


def _render_field(
    mol: Chem.Mol,
    weights: np.ndarray,
    norm: Normalize,
    cmap: Colormap,
    size: tuple[int, int],
    label_indices: bool,
    background: str,
    alpha: float,
) -> bytes:
    """RDKit Gaussian contour field (similarity-map style)."""
    drawer = rdMolDraw2D.MolDraw2DCairo(*size)
    opts = drawer.drawOptions()
    opts.addAtomIndices = label_indices
    opts.clearBackground = True
    opts.setBackgroundColour((1, 1, 1, 1))
    # scale so the field uses the same symmetric range as the colour bar
    scale = float(norm.vmax)
    SimilarityMaps.GetSimilarityMapFromWeights(
        mol,
        [float(w) for w in weights],
        draw2d=drawer,
        # RDKit only reads three anchors off a colormap, and its "is this a
        # matplotlib colormap" test is an isinstance against
        # LinearSegmentedColormap -- which a ListedColormap (e.g. anything
        # from trim_colormap) fails, landing it in the subscript branch.
        # Hand over the anchors directly and the type stops mattering.
        colorMap=[tuple(cmap(x)) for x in (0.0, 0.5, 1.0)],
        scale=scale,
        contourLines=6,
        alpha=alpha,
        # without this the whole grid is filled with the colormap's midpoint
        # colour, which paints a grey rectangle behind the molecule
        useFillThreshold=True,
        fillThreshold=0.06,
        fillThresholdIsFraction=True,
    )
    drawer.FinishDrawing()
    return drawer.GetDrawingText()


def draw_atom_attributions(
    mol,
    atom_weights: Sequence[float],
    *,
    bond_weights: Sequence[float] | None = None,
    mode: str = "atoms",
    prediction: float | None = None,
    prediction_label: str = "prediction",
    title: str | None = None,
    subtitle: str | None = None,
    cmap: str | Colormap = ATTRIBUTION_CMAP,
    vmax: float | None = None,
    size: tuple[int, int] = (520, 420),
    show_colorbar: bool = True,
    colorbar_label: str = "attribution to prediction",
    label_indices: bool = False,
    annotate_top_k: int = 0,
    highlight_radius: float = 0.42,
    alpha: float | None = None,
    background: str = "white",
    colorbar_side: str = "right",
    colorbar_width: str = "4.5%",
    colorbar_pad: float = 0.22,
    ax: plt.Axes | None = None,
):
    """Draw a per-atom attribution map.

    Parameters
    ----------
    mol
        RDKit Mol or SMILES string.
    atom_weights
        One scalar per heavy atom, in RDKit atom-index order. Sign is
        meaningful: positive = pushes the prediction up.
    bond_weights
        Optional scalar per bond, in RDKit bond-index order, sharing the
        colour scale with ``atom_weights``. Only used by ``mode="atoms"``;
        the contour field has no bond channel to paint. Without it bonds
        are shaded by the mean of their endpoints, which looks like data
        but is only interpolation.
    mode
        "atoms" (discrete node colouring) or "field" (Gaussian contours).
    prediction
        Optional scalar model output, printed in the caption.
    vmax
        Fix the colour-scale limit. Pass the *same* value across a set of
        molecules if you intend to compare them by eye; otherwise each
        map is self-normalised and cross-molecule comparison is invalid.
    annotate_top_k
        Print atom indices of the k largest-|w| atoms in the caption.
    alpha
        Opacity of the colour overlay in ``[0, 1]``. Defaults to 1.0 for
        ``mode="atoms"`` and 0.35 for ``mode="field"``, whose contours
        otherwise bury the structure. Lower it to keep bonds and atom
        labels readable; note that it changes only the overlay, so a faded
        colour no longer matches the colour bar exactly.
    background
        "white" (solid, composited) or "transparent" (alpha 0). Never a
        near-white grey -- the contour renderer's default midpoint fill is
        explicitly suppressed.
    colorbar_side
        "right" (default) or "left". Ticks and label follow the bar.
    ax
        Draw into an existing Axes (for multi-panel figures). If None a
        new Figure is created and returned.

    Returns
    -------
    matplotlib Figure
    """
    mol = prepare_mol(mol)
    weights = np.asarray(atom_weights, dtype=float)

    if weights.shape[0] != mol.GetNumAtoms():
        raise ValueError(
            f"got {weights.shape[0]} weights for {mol.GetNumAtoms()} atoms; "
            "attributions must be aligned to RDKit atom indices"
        )
    if not np.all(np.isfinite(weights)):
        raise ValueError("attribution vector contains NaN/inf")

    bonds = None
    if bond_weights is not None:
        bonds = np.asarray(bond_weights, dtype=float)
        if bonds.shape[0] != mol.GetNumBonds():
            raise ValueError(
                f"got {bonds.shape[0]} bond weights for {mol.GetNumBonds()} bonds; "
                "attributions must be aligned to RDKit bond indices"
            )
        if not np.all(np.isfinite(bonds)):
            raise ValueError("bond attribution vector contains NaN/inf")

    cmap = colormaps[cmap] if isinstance(cmap, str) else cmap
    # one scale over both channels, so an atom and a bond of the same colour
    # really did contribute the same amount
    norm = _symmetric_norm(weights if bonds is None else np.concatenate([weights, bonds]), vmax)

    if alpha is not None and not 0.0 <= alpha <= 1.0:
        raise ValueError(f"alpha must be in [0, 1], got {alpha}")

    if mode == "atoms":
        png = _render_atoms(
            mol,
            weights,
            bonds,
            norm,
            cmap,
            size,
            label_indices,
            highlight_radius,
            background,
            1.0 if alpha is None else alpha,
        )
    elif mode == "field":
        if bonds is not None:
            raise ValueError(
                "mode='field' has no bond channel; fold the bond attributions into "
                "atoms first (see MolAttribution.plot(bonds='fold'))"
            )
        png = _render_field(
            mol,
            weights,
            norm,
            cmap,
            size,
            label_indices,
            background,
            0.35 if alpha is None else alpha,
        )
    else:
        raise ValueError("mode must be 'atoms' or 'field'")

    img = _png_to_array(png, background=background)
    h, w_px = img.shape[:2]

    has_caption = bool(subtitle) or prediction is not None or annotate_top_k
    extra_in = (0.75 if has_caption else 0.0) + (0.35 if title else 0.0)

    owns_fig = ax is None
    if owns_fig:
        width_in = size[0] / 100
        fig, ax = plt.subplots(figsize=(width_in, width_in * h / w_px + extra_in))
        fig.patch.set_alpha(0.0 if background == "transparent" else 1.0)
        if background == "white":
            fig.patch.set_facecolor("white")
    else:
        fig = ax.figure

    ax.imshow(img)
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)

    if title:
        ax.set_title(title, fontsize=10, weight="bold", pad=6, wrap=True)

    caption = []
    if subtitle:
        caption.append(subtitle)
    if prediction is not None and isinstance(prediction, (int, float)):
        caption.append(f"{prediction_label} = {prediction:.2f}")
    if prediction is not None and isinstance(prediction, (list, np.ndarray, tuple)):
        prediction_str = ", ".join(f"{p:.2f}" for p in prediction)
        caption.append(f"{prediction_label} = [{prediction_str}]")
    if annotate_top_k:
        order = np.argsort(-np.abs(weights))[:annotate_top_k]
        top = ", ".join(
            f"{mol.GetAtomWithIdx(int(i)).GetSymbol()}{int(i)} {weights[i]:+.2f}" for i in order
        )
        caption.append(f"largest |w|:  {top}")
    if caption:
        ax.set_xlabel("\n".join(caption), fontsize=8, labelpad=8, linespacing=1.5)

    if show_colorbar:
        if colorbar_side not in ("left", "right"):
            raise ValueError("colorbar_side must be 'left' or 'right'")
        sm = ScalarMappable(norm=norm, cmap=cmap)
        # append_axes ties the bar to this Axes, so it flanks the structure
        # and matches its height exactly
        cax = make_axes_locatable(ax).append_axes(
            colorbar_side, size=colorbar_width, pad=colorbar_pad
        )
        cbar = fig.colorbar(sm, cax=cax)
        cax.yaxis.set_ticks_position(colorbar_side)
        cax.yaxis.set_label_position(colorbar_side)
        if colorbar_label:
            cbar.set_label(colorbar_label, fontsize=8)
        cbar.ax.tick_params(labelsize=7)
        cbar.outline.set_linewidth(0.5)

    if owns_fig:
        fig.tight_layout(pad=0.3)
    return fig


def _panel_entry(entry) -> tuple[Chem.Mol, MolAttribution]:
    """Normalise one panel value to ``(mol, attribution)``.

    A MolAttribution already knows its own structure, so a bare one is the
    normal case; the ``(mol, attribution)`` form is the escape hatch for
    attributions computed on a pre-featurized input (``smiles is None``)
    or for drawing one on a different depiction.
    """
    if isinstance(entry, MolAttribution):
        return entry.molecule(), entry
    mol, attribution = entry
    return attribution.molecule(mol), attribution


def draw_attribution_panel(
    panels: dict[str, MolAttribution | tuple[str | Chem.Mol, MolAttribution]],
    *,
    shared_scale: bool = True,
    bonds: str = "own",
    mode: str = "atoms",
    cmap: str | Colormap = ATTRIBUTION_CMAP,
    alpha: float | None = None,
    size: tuple[int, int] = (460, 380),
    suptitle: str | None = None,
    background: str = "white",
    **kwargs,
):
    """Several attributions side by side.

    Parameters
    ----------
    panels
        ``{column title: attribution}``. Each MolAttribution carries the
        molecule it was computed on, so the structure does not have to be
        passed alongside it. A value may also be a
        ``(molecule, attribution)`` pair -- a SMILES string or RDKit Mol
        plus the MolAttribution -- which is what to use when the attribution
        has ``smiles=None`` (a pre-featurized input), or when this panel
        should draw a different depiction from the one the MolAttribution
        names. The numbers, the prediction in the caption and the
        atom/bond indexing always come from the MolAttribution.
    shared_scale
        Put every panel on one symmetric colour scale (and draw a single
        colour bar). Panels are only comparable by eye when this is True;
        with False each panel is self-normalised.
    bonds
        ``"own"`` / ``"fold"`` / ``"ignore"``, exactly as in
        :meth:`MolAttribution.plot`. Applied to every panel, so the columns
        stay comparable.
    alpha
        Overlay opacity, as in :func:`draw_atom_attributions`. One value
        for all panels: a per-panel opacity would make identical
        attributions look different from column to column.

    Returns
    -------
    matplotlib Figure
    """
    if not panels:
        raise ValueError("panels is empty")

    names = list(panels)
    resolved = {}
    for name in names:
        mol, attribution = _panel_entry(panels[name])
        resolved[name] = (
            mol,
            *attribution.weights_for(bonds, mol),
            attribution.prediction,
        )

    vmax = None
    if shared_scale:
        # over both channels of every panel, so equal colours across the
        # figure really do mean equal contributions
        all_w = np.concatenate(
            [
                np.concatenate([atoms] + ([] if bws is None else [np.asarray(bws, float)]))
                for _, atoms, bws, _ in resolved.values()
            ]
        )
        vmax = float(np.max(np.abs(all_w))) or 1.0

    fig, axes = plt.subplots(
        1,
        len(names),
        figsize=(size[0] / 100 * len(names) + 1.2, size[1] / 100 + 1.0),
    )
    fig.patch.set_alpha(0.0 if background == "transparent" else 1.0)
    if background == "white":
        fig.patch.set_facecolor("white")
    if len(names) == 1:
        axes = [axes]

    kwargs.pop("show_colorbar", None)
    for i, (ax, name) in enumerate(zip(axes, names, strict=True)):
        mol, atoms, bws, prediction = resolved[name]
        draw_atom_attributions(
            mol,
            atoms,
            bond_weights=bws,
            mode=mode,
            cmap=cmap,
            alpha=alpha,
            vmax=vmax,
            size=size,
            background=background,
            title=name,
            prediction=prediction,
            # one bar for the whole panel when the scale is shared, so the
            # figure cannot be misread as each panel having its own range
            show_colorbar=(not shared_scale) or (i == len(names) - 1),
            ax=ax,
            **kwargs,
        )

    if suptitle:
        fig.suptitle(suptitle, fontsize=12, weight="bold")
    fig.tight_layout()
    return fig


def draw_molecule(
    mol,
    *,
    size: tuple[int, int] = (520, 420),
    background: str = "white",
    label_indices: bool = False,
    title: str | None = None,
    highlight_atoms: dict[int, tuple[float, float, float]] | Sequence[int] | None = None,
    highlight_bonds: bool = True,
    atom_notes: dict[int, str] | None = None,
    as_figure: bool = True,
):
    """The same structure with no attribution overlay.

    Worth producing alongside every attribution map: it is the control that
    lets a reader see which visual features come from the molecule and which
    from the model. Uses the identical depiction code path, so the two
    images are registered atom-for-atom.

    Parameters
    ----------
    highlight_atoms
        Atoms to mark, either as a plain sequence of indices or as
        ``{atom index: RGB}`` when different atoms should carry different
        colours. This is *annotation*, not attribution: use it to point at
        a substructure known from the literature, never to show what a
        model computed -- that is what
        :func:`draw_atom_attributions` is for, and it comes with a scale.
    highlight_bonds
        Also shade bonds whose two atoms are both highlighted, so a marked
        ring reads as one unit rather than a string of dots. Bonds take the
        colour of their first endpoint.
    atom_notes
        ``{atom index: text}`` drawn next to the atom, e.g. to name the
        ring position being pointed at.

    Returns a matplotlib Figure (``as_figure=True``) or raw PNG bytes.
    """
    mol = prepare_mol(mol)

    if highlight_atoms is None:
        atom_colors = {}
    elif isinstance(highlight_atoms, dict):
        atom_colors = {int(i): tuple(c) for i, c in highlight_atoms.items()}
    else:
        atom_colors = {int(i): (0.85, 0.33, 0.10) for i in highlight_atoms}

    bond_colors = {}
    if highlight_bonds:
        for bond in mol.GetBonds():
            begin, end = bond.GetBeginAtomIdx(), bond.GetEndAtomIdx()
            if begin in atom_colors and end in atom_colors:
                bond_colors[bond.GetIdx()] = atom_colors[begin]

    drawer = rdMolDraw2D.MolDraw2DCairo(*size)
    opts = drawer.drawOptions()
    opts.clearBackground = True
    opts.setBackgroundColour((1, 1, 1, 0 if background == "transparent" else 1))
    opts.addAtomIndices = label_indices
    opts.bondLineWidth = 2
    opts.fillHighlights = True
    opts.highlightRadius = 0.42
    opts.highlightBondWidthMultiplier = 16
    opts.annotationFontScale = 0.7
    for idx, note in (atom_notes or {}).items():
        mol.GetAtomWithIdx(int(idx)).SetProp("atomNote", note)

    rdMolDraw2D.PrepareAndDrawMolecule(
        drawer,
        mol,
        highlightAtoms=list(atom_colors),
        highlightAtomColors=atom_colors,
        highlightBonds=list(bond_colors),
        highlightBondColors=bond_colors,
    )
    drawer.FinishDrawing()
    png = drawer.GetDrawingText()

    if not as_figure:
        return png

    img = _png_to_array(png, background=background)
    h, w_px = img.shape[:2]
    width_in = size[0] / 100
    fig, ax = plt.subplots(figsize=(width_in, width_in * h / w_px + (0.35 if title else 0.0)))
    fig.patch.set_alpha(0.0 if background == "transparent" else 1.0)
    if background == "white":
        fig.patch.set_facecolor("white")
    ax.imshow(img)
    ax.set_axis_off()
    if title:
        ax.set_title(title, fontsize=10, weight="bold", pad=6)
    fig.tight_layout(pad=0.2)
    return fig


def _render_fragment_in_context(
    mol: Chem.Mol,
    atoms: Sequence[int],
    bonds: Sequence[int],
    color: tuple[float, float, float],
    size: tuple[int, int],
    background: str,
    dim_context: bool,
) -> bytes:
    """One exemplar molecule with a circular environment filled in."""
    drawer = rdMolDraw2D.MolDraw2DCairo(*size)
    opts = drawer.drawOptions()
    opts.clearBackground = True
    opts.setBackgroundColour((1, 1, 1, 0 if background == "transparent" else 1))
    opts.fillHighlights = True
    opts.highlightRadius = 0.42
    opts.highlightBondWidthMultiplier = 16
    opts.bondLineWidth = 2
    if dim_context:
        # the exemplar is scaffolding: it says *where* the fragment sits,
        # not what the model looked at. Drawing it monochrome leaves the
        # only colour in the cell on the highlighted environment, which is
        # the part the bit actually means.
        opts.useBWAtomPalette()

    rdMolDraw2D.PrepareAndDrawMolecule(
        drawer,
        mol,
        highlightAtoms=[int(a) for a in atoms],
        highlightAtomColors={int(a): color for a in atoms},
        highlightBonds=[int(b) for b in bonds],
        highlightBondColors={int(b): color for b in bonds},
    )
    drawer.FinishDrawing()
    return drawer.GetDrawingText()


def draw_bit_attributions(
    bit_values: Sequence[tuple[int, float]] | dict[int, float],
    bit_dictionary,
    *,
    ncols: int = 3,
    cmap: str | Colormap = ATTRIBUTION_CMAP,
    vmax: float | None = None,
    size: tuple[int, int] = (300, 250),
    background: str = "white",
    suptitle: str | None = None,
    show_colorbar: bool = True,
    colorbar_label: str = "attribution to prediction",
    dim_context: bool = True,
    skip_unknown: bool = True,
):
    """Draw attributions that live on fingerprint *bits*, not on atoms.

    :func:`draw_atom_attributions` can only colour substructures the
    molecule has. The attribution a model puts on a bit that is *off*
    has no atom to sit on, so it never survives the projection onto the graph
    (see :meth:`~talktorial_xai.attribution.FingerprintAttribution.to_mol_attribution`).

    This function draws those bits instead, one cell each, by borrowing a
    training molecule that *does* contain the substructure from a
    :class:`~talktorial_xai.bit_dictionary.BitDictionary` and highlighting
    the environment in it. Read a cell as "this is what the model was
    looking for", with the colour saying which way the verdict went -- not
    as a claim about the molecule being explained, which contains none of
    what is drawn.

    Parameters
    ----------
    bit_values
        ``[(bit, attribution), ...]`` or ``{bit: attribution}``, already
        selected and ordered -- normally straight from
        :meth:`~talktorial_xai.attribution.FingerprintAttribution.absent_bits`
        or :meth:`BitDictionary.rank_bits`.
    bit_dictionary
        The :class:`~talktorial_xai.bit_dictionary.BitDictionary` built
        over the model's training set. Its exemplars are what gets drawn.
    vmax
        Fix the colour-scale limit, e.g. to the ``vmax`` used for the atom
        map of the same molecule. Pass it whenever the two figures are
        shown side by side, or the absent bits will look stronger or
        weaker than the present ones for no reason.
    dim_context
        Draw the exemplar molecule monochrome so only the environment
        carries colour.
    skip_unknown
        Silently drop bits the dictionary has no exemplar for (they cannot
        be drawn). With False, such a bit raises.

    Returns
    -------
    matplotlib Figure
    """
    items = list(bit_values.items()) if isinstance(bit_values, dict) else list(bit_values)
    cells = []
    for bit, value in items:
        record = bit_dictionary.get(int(bit))
        if record is None or not record.fragments:
            if skip_unknown:
                continue
            raise ValueError(f"bit {bit} has no exemplar in the dictionary; cannot draw it")
        cells.append((int(bit), float(value), record))

    if not cells:
        raise ValueError("nothing to draw: no bit had an exemplar in the dictionary")

    cmap = colormaps[cmap] if isinstance(cmap, str) else cmap
    norm = _symmetric_norm(np.array([v for _, v, _ in cells], dtype=float), vmax)

    ncols = max(1, min(ncols, len(cells)))
    nrows = -(-len(cells) // ncols)
    fig, axes = plt.subplots(
        nrows,
        ncols,
        figsize=(size[0] / 100 * ncols + 1.2, (size[1] / 100 + 0.95) * nrows + 0.5),
        squeeze=False,
    )
    fig.patch.set_alpha(0.0 if background == "transparent" else 1.0)
    if background == "white":
        fig.patch.set_facecolor("white")

    flat = axes.ravel()
    for ax, (bit, value, record) in zip(flat, cells, strict=False):
        fragment = record.top_fragment
        mol = prepare_mol(fragment.molecule())
        atoms, bonds = fragment.atoms(mol)
        png = _render_fragment_in_context(
            mol,
            atoms,
            bonds,
            tuple(cmap(norm(value))[:3]),
            size,
            background,
            dim_context,
        )
        # uncropped, so every cell keeps the same aspect ratio and the
        # grid's titles line up row by row
        ax.imshow(_png_to_array(png, background=background, crop=False))
        ax.set_xticks([])
        ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_visible(False)
        ax.set_title(f"bit {bit}   {value:+.3f}", fontsize=10, weight="bold", pad=5)
        ax.set_xlabel(
            f"{fragment.smiles}   (r={fragment.radius})\n"
            f"in {bit_dictionary.frequency(bit):.0%} of training set"
            f"   ·   purity {record.purity:.0%}",
            fontsize=8,
            labelpad=6,
            linespacing=1.5,
        )

    for ax in flat[len(cells) :]:
        ax.set_axis_off()

    if suptitle:
        fig.suptitle(suptitle, fontsize=12, weight="bold")
    fig.tight_layout()

    if show_colorbar:
        sm = ScalarMappable(norm=norm, cmap=cmap)
        cbar = fig.colorbar(sm, ax=list(flat), fraction=0.03, pad=0.02)
        if colorbar_label:
            cbar.set_label(colorbar_label, fontsize=8)
        cbar.ax.tick_params(labelsize=7)
        cbar.outline.set_linewidth(0.5)

    return fig


def save(fig, path, dpi: int = 200, background: str = "white") -> None:
    """savefig with the transparency setting that matches ``background``."""
    fig.savefig(
        path,
        dpi=dpi,
        bbox_inches="tight",
        pad_inches=0.05,
        transparent=(background == "transparent"),
        facecolor="white" if background == "white" else "none",
    )
