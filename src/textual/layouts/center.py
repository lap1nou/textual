from __future__ import annotations

from fractions import Fraction

from ..geometry import Size, Region
from .._layout import ArrangeResult, Layout, WidgetPlacement
from ..widget import Widget


class CenterLayout(Layout):
    """Positions widgets in the center of the screen."""

    name = "center"

    def arrange(
        self, parent: Widget, children: list[Widget], size: Size
    ) -> ArrangeResult:

        placements: list[WidgetPlacement] = []
        total_regions: list[Region] = []

        parent_size = parent.outer_size
        container_width, container_height = size
        fraction_unit = Fraction(size.width)

        for widget in children:
            width, height, margin = widget.get_box_model(
                size, parent_size, fraction_unit
            )
            margin_width = width + margin.width
            margin_height = height + margin.height
            x = margin.left + max(0, (container_width - margin_width) // 2)
            y = margin.top + max(0, (container_height - margin_height) // 2)
            region = Region(x, y, int(width), int(height))
            total_regions.append(region.grow(margin))
            placements.append(WidgetPlacement(region, widget, 0))

        placements.append(WidgetPlacement(Region.from_union(total_regions), None, 0))
        return placements, set(children)
