from typing import Mapping

from markdown_it import MarkdownIt
from markdown_it.rules_block import StateBlock
from mdformat import renderer
from mdformat.renderer import RenderContext, RenderTreeNode
from mdformat.renderer.typing import Render


def update_mdit(mdit: MarkdownIt) -> None:
    """
    Skip pairs before the first empty line
    """

    front_matter = make_front_matter_rule()
    mdit.block.ruler.before(
        "table",
        "front_matter",
        front_matter,
        {"alt": ["paragraph", "reference", "blockquote", "list"]},
    )


def make_front_matter_rule():
    def front_matter(state: StateBlock, start_line: int, end_line: int, silent: bool):
        # grab initial data if it's : separated
        if start_line != 0:
            return False

        # Since start is found, we can report success here in validation mode
        # if silent:
        #    return True

        # Search for the end of the block
        next_line = start_line
        start_content = 0
        meta = {}

        while True:
            next_line += 1
            if next_line >= end_line:
                # unclosed block should be autoclosed by end of document.
                return False

            start = state.bMarks[next_line]
            maximum = state.eMarks[next_line]

            if start == maximum:
                # empty line is terminator
                break

            key_value = state.src[start:maximum].split(":", 1)
            if len(key_value) != 2:
                # Error here, we have no k/v separator
                return False
            meta[key_value[0].lower()] = key_value[1]
        old_parent = state.parentType
        old_line_max = state.lineMax
        state.parentType = "container"

        # this will prevent lazy continuations from ever going past our end marker
        state.lineMax = next_line

        token = state.push("pelican_frontmatter", "", 0)
        # token.hidden = True
        token.content = state.src[state.bMarks[start_content] : state.eMarks[next_line]]
        token.block = True
        token.meta = meta

        state.parentType = old_parent
        state.lineMax = old_line_max
        state.line = next_line
        token.map = [start_line, state.line]

        # consider taking the content into a dictionary and checking for Title: .+\n

        return True

    return front_matter


def _pelican_frontmatter_renderer(node: RenderTreeNode, context: RenderContext) -> str:
    return node.content.rstrip()


# Precompute the pelican placeholders to avoid doing it on every render.
# Supports both the standard curly braces and the deprecated pipe characters as delimiters:
# - %7B -> {
# - %7D -> }
# - %7C -> |
PLACEHOLDERS: [str, str] = {
    start + keyword + end: "{" + keyword + "}"
    for keyword in (
        "author",
        "category",
        "index",
        "tag",
        "filename",
        "static",
        "attach",
    )
    for start, end in (("%7B", "%7D"), ("%7C", "%7C"))
}


def replace_pelican_placeholdlers(original_url: str) -> str:
    new_url = original_url
    for placeholder, replacement in PLACEHOLDERS.items():
        new_url = new_url.replace(placeholder, replacement)
    return new_url


def _pelican_image_renderer(node: RenderTreeNode, context: RenderContext) -> str:
    node.attrs["src"] = replace_pelican_placeholdlers(node.attrs["src"])
    return renderer.DEFAULT_RENDERERS.get("image")(node, context)


def _pelican_link_open_renderer(node: RenderTreeNode, context: RenderContext) -> str:
    node.attrs["href"] = replace_pelican_placeholdlers(node.attrs["href"])
    return renderer.DEFAULT_RENDERERS.get("link")(node, context)


RENDERERS: Mapping[str, Render] = {
    "pelican_frontmatter": _pelican_frontmatter_renderer,
    "image": _pelican_image_renderer,
}


# XXX mdformat-pelican and mdformat-gfm plugins are not compatible. See:
# https://github.com/hukkin/mdformat-gfm/issues/38
# https://github.com/gaige/mdformat-pelican/issues/3
# So we're going to monkey-patch mdformat_gfm's link rendering.
try:
    import mdformat_gfm

    def _patch_gfm_link_renderer(node: RenderTreeNode, context: RenderContext) -> str:
        """Patched link renderer that replaces pelican placeholders in link's href."""
        if any((bad_placeholder in node.attrs["href"]) for bad_placeholder in PLACEHOLDERS):
            node.attrs["href"] = replace_pelican_placeholdlers(node.attrs["href"])
        # Use the original renderer.
        return mdformat_gfm.plugin._link_renderer(node, context)

    # Use our patched renderer instead of mdfomat_gfm's.
    mdformat_gfm.plugin.RENDERERS["link"] = _patch_gfm_link_renderer

# Register the link renderer the usual way if the gfm plugin is not installed.
except ImportError:
    RENDERERS["link"] = _pelican_link_open_renderer
