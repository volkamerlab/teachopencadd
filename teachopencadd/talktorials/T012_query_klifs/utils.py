"""
Utilities helpful in the context of Jupyter Notebooks
"""

from IPython.display import display as _display, HTML as _HTML, Markdown as _Markdown


def _alert(contents, style):
    return "\n\n".join([f'<div class="alert alert-block alert-{style}">', contents, "</div>"])


def _hidden(contents, summary):
    return "\n\n".join([f"<details>", f"<summary>{summary}</summary>", contents, "</details>"])


def _rich_print(*args, engine=_Markdown, sep=" ", alert=None, hidden=None, display=True, **kwargs):
    r"""
    Displays rich Markdown output
    Parameters
    ----------
    args : str
        Markdown-formatted text to be rendered
    sep : str, optional=" "
        Default separator between items in `args`. Take into account
        that \n and similar might be processed into whitespace by the
        renderer!
    alert : str, optional=None
        Colored box style. Must be one of info, warning, success or danger.
    hidden : str, optional=None
        If set, use value as the title of a collapsed box that can be revealed
        on click.
    display: bool, optional=True
        Whether to display rendered output right away or return just the output
    """
    contents = sep.join([str(a) for a in args])
    if alert is not None:
        contents = _alert(contents, alert)
    if hidden is not None:
        contents = _hidden(contents, hidden)
    out = engine(contents, **kwargs)
    if display:
        return _display(out)
    return out


def print_html(*args, sep=" ", alert=None, hidden=None, display=True, **kwargs):
    r"""
    Displays rich HTML output
    Parameters
    ----------
    args : str
        HTML text to be rendered
    sep : str, optional=" "
        Default separator between items in `args`. Take into account
        that \n and similar will be processed into whitespace by the
        renderer!
    display: bool, optional=True
        Whether to display rendered output right away or return just the output
    alert : str, optional=None
        Colored box style. Must be one of info, warning, success or danger.
    hidden : str, optional=None
        If set, use value as the title of a collapsed box that can be revealed
        on click.
    """
    return _rich_print(
        *args, engine=_HTML, sep=sep, alert=alert, hidden=hidden, display=display, **kwargs
    )


hprint = print_html


def print_markdown(
    *args, sep=" ", alert=None, hidden=None, display=True, process_newlines=True, **kwargs
):
    r"""
    Displays rich Markdown output
    Parameters
    ----------
    args : str
        Markdown-formatted text to be rendered
    sep : str, optional=" "
        Default separator between items in `args`. Take into account
        that \n and similar will be processed into whitespace by the
        renderer!
    display: bool, optional=True
        Whether to display rendered output right away or return just the output
    alert : str, optional=None
        Colored box style. Must be one of info, warning, success or danger.
    hidden : str, optional=None
        If set, use value as the title of a collapsed box that can be revealed
        on click.
    process_newlines : bool, optional=True
        If [\r]\n is present, replace with <br />  tags to mimic `print` as much
        as possible. This also applies to the value of `sep`. This does not apply
        for contents that contain blank lines.
    """
    if process_newlines:
        contents = sep.join(args)
        if "\r\n\r\n" not in contents:
            contents = contents.replace("\r\n", "<br />")
        if "\n\n" not in contents:
            contents = contents.replace("\n", "<br />")
        args = (contents,)

    return _rich_print(
        *args, engine=_Markdown, sep=sep, alert=alert, hidden=hidden, display=display, **kwargs
    )


mprint = print_markdown 