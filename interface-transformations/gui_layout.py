from tkinter import CENTER, END, Entry, Frame, Label, Menubutton, W


def make_entry(parent, width=5):
    """Create a centered Entry widget with the given width."""
    entry = Entry(parent, justify=CENTER)
    entry["width"] = width
    return entry


def place_entry(parent, row, padx, default, width=5, sticky="w", pady=(10, 2)):
    """Create, position, and initialize a centered Entry widget in one call."""
    entry = make_entry(parent, width)
    entry.grid(row=row, column=0, sticky=sticky, padx=padx, pady=pady)
    entry.delete(0, END)
    entry.insert(0, str(default))
    return entry


def _normalize_padding(padding):
    if isinstance(padding, str):
        padding = padding.split()
    if isinstance(padding, (tuple, list)):
        if not padding:
            return (0, 0)
        if len(padding) == 1:
            value = int(padding[0])
            return (value, value)
        return (int(padding[0]), int(padding[1]))
    value = int(padding) if padding else 0
    return (value, value)


def _left_padding(widget):
    return _normalize_padding(widget.grid_info().get("padx", 0))[0]


def _row_sort_key(item):
    _, widget = item
    info = widget.grid_info()
    return (_left_padding(widget), int(info.get("column", 0)), item[0])


def _default_sticky(widget):
    return "ew" if isinstance(widget, (Entry, Menubutton)) else "w"


def apply_responsive_grid(container):
    children = [child for child in container.winfo_children() if child.winfo_manager() == "grid"]

    rows = {}
    for index, child in enumerate(children):
        row = int(child.grid_info().get("row", 0))
        rows.setdefault(row, []).append((index, child))

    max_columns = 1
    stretch_columns = set()
    separators = []

    for row in sorted(rows):
        row_items = sorted(rows[row], key=_row_sort_key)
        row_widgets = [widget for _, widget in row_items]

        if len(row_widgets) == 1 and isinstance(row_widgets[0], Frame):
            separators.append((row, row_widgets[0]))
            continue

        for logical_column, widget in enumerate(row_widgets):
            info = widget.grid_info()
            pady = _normalize_padding(info.get("pady", 0))
            widget.grid_configure(
                row=row,
                column=logical_column,
                padx=(5, 5),
                pady=pady,
                sticky=_default_sticky(widget),
            )

            if isinstance(widget, (Entry, Menubutton)):
                stretch_columns.add(logical_column)

        max_columns = max(max_columns, len(row_widgets))

    for row, widget in separators:
        pady = _normalize_padding(widget.grid_info().get("pady", 0))
        widget.grid_configure(
            row=row,
            column=0,
            columnspan=max_columns,
            padx=(5, 5),
            pady=pady,
            sticky="ew",
        )

    for column in range(max_columns):
        container.grid_columnconfigure(column, weight=1 if column in stretch_columns else 0)
