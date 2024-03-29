#!/usr/bin/env python3

"""
Stanford CS106A BabyNames Project
Part-B: graphics GUI built on the baby data
"""

import sys
import tkinter
import babynames


# Provided constants to load and draw the baby data
FILENAMES = ['baby-1900.txt', 'baby-1910.txt', 'baby-1920.txt', 'baby-1930.txt',
             'baby-1940.txt', 'baby-1950.txt', 'baby-1960.txt', 'baby-1970.txt',
             'baby-1980.txt', 'baby-1990.txt', 'baby-2000.txt', 'baby-2010.txt',
             'baby-2020.txt']

YEARS = [1900, 1910, 1920, 1930, 1940, 1950, 1960, 1970, 1980, 1990, 2000,
         2010, 2020]
SPACE = 20
COLORS = ['red', 'purple', 'green']
TEXT_DX = 2
LINE_WIDTH = 2
MAX_RANK = 1000


def compute_x(width, year_index):
    """
    Given canvas width and year_index 0, 1, 2 .. into YEARS list,
    return the x value for the vertical line for that year.
    """

    return (width - 2 * SPACE) / len(YEARS) * year_index + SPACE


def draw_fixed(canvas):
    """
    Erases the given canvas and draws the fixed lines on it.
    """

    canvas.delete('all')
    width = canvas.winfo_width()
    height = canvas.winfo_height()

    canvas.create_line(0 + SPACE, 0 + SPACE, width - SPACE, 0 + SPACE)
    canvas.create_line(0 + SPACE, height - SPACE, width - SPACE, height - SPACE)

    for i in range(len(YEARS)):
        canvas.create_line(compute_x(width, i), 0, compute_x(width, i), height)

    for i in range(len(YEARS)):
        x = compute_x(width, i)
        canvas.create_text(x, height - SPACE, text=YEARS[i], anchor=tkinter.NW)


def compute_rank(names, name, year):
    """
    Given names dict, name string, and int year e.g. 1900.
    Return the best rank to use: the actual rank if
    that name+year exists in the data, or MAX_RANK
    if the name or year is not present.
    >>> # Tests provided, code TBD
    >>> compute_rank({'Abe': {1900: 100}}, 'Abe', 1900)
    100
    >>> compute_rank({'Abe': {1900: 100}}, 'Abe', 2020)
    1000
    >>> compute_rank({'Abe': {1900: 100}}, 'Alice', 1900)
    1000
    """

    if name in names:
        years = names[name]
        if year in years:
            return years[year]

    if name not in names:
        return MAX_RANK
    years = names[name]

    if year not in years:
        return MAX_RANK

    return MAX_RANK


def compute_y(names, name, height, year_index):
    """
    Given names dict, name string, canvas height, and
    year_index 0 1 2 ..., compute and return the y for
    the that name/year_index line endpoint.
    """

    y = compute_rank(names, name, YEARS[year_index])
    start = ((height - 2 * SPACE) / MAX_RANK) * y + SPACE
    return start

def draw_name(canvas, names, name, color):
    """
    Given canvas, and names dict.
    Draw the data for the given name in the given color.
    """

    width = canvas.winfo_width()
    height = canvas.winfo_height()

    for i in range(len(YEARS)):
        x1 = compute_x(width, i)
        y1 = compute_y(names, name, height, i)

        rank = str(compute_rank(names, name, YEARS[i]))
        canvas.create_text(x1 + TEXT_DX, y1, text=name + ' ' + str(rank), fill=color, anchor=tkinter.SW)

        if i < len(YEARS) - 1:
            x2 = compute_x(width, i + 1)
            y2 = compute_y(names, name, height, i + 1)

            canvas.create_line(x1, y1, x2, y2, width=LINE_WIDTH, fill=color)


def draw_names(canvas, names, lookups):
    """
    Given canvas, names dict, lookups list of name strings,
    Draw the data for the lookups on the canvas.
    """

    draw_fixed(canvas)
    for i in range(len(lookups)):
        if i != 0:
            hey = i % len(COLORS)
            draw_name(canvas, names, lookups[i], COLORS[hey])
        else:
            draw_name(canvas, names, lookups[i], COLORS[0])

def upper_name(name):
    """
    (provided)
    The names in the SSA data set all have their first
    char uppercase, then lowercase e.g. 'Emily'.
    Given a name typed by the user, change its case
    to the SSA form.
    >>> upper_name('emily')
    'Emily'
    >>> upper_name('EMILY')
    'Emily'
    """

    if len(name) > 0:
        return name[0].upper() + name[1:].lower()
    return name


def make_gui(top, width, height, names):
    """
    (provided)
    Set up the GUI elements for Baby Names, returning the TK Canvas to use.
    top is TK root, width/height is canvas size, names is BabyNames dict.
    """

    # name entry field
    entry = tkinter.Entry(top, width=60, name='entry', borderwidth=2)
    entry.grid(row=0, columnspan=12, sticky='w')
    entry.focus()

    # canvas for drawing
    canvas = tkinter.Canvas(top, width=width, height=height, name='canvas')
    canvas.grid(row=1, columnspan=12, sticky='w')

    space = tkinter.LabelFrame(top, width=10, height=10, borderwidth=0)
    space.grid(row=2, columnspan=12, sticky='w')

    # Search field etc. at the bottom
    label = tkinter.Label(top, text='Search:')
    label.grid(row=3, column=0, sticky='w')
    search_entry = tkinter.Entry(top, width=15, name='searchentry')
    search_entry.grid(row=3, column=1, sticky='w')
    search_out = tkinter.Text(top, height=3, width=70, name='searchout', borderwidth=2)
    search_out.grid(row=3, column=3, sticky='w')

    # When <return> key is hit in a text field .. connect to the handle_draw()
    # and handle_search() functions to do the work.
    entry.bind('<Return>', lambda event: handle_draw(entry, canvas, names))
    search_entry.bind('<Return>', lambda event: handle_search(search_entry, search_out, names))

    top.update()
    return canvas


def handle_draw(entry, canvas, names):
    """
    (provided)
    Called when <return> key hit in given text entry field.
    Gets search text, looks up names, calls draw_names()
    for those names to draw the results.
    """

    text = entry.get()
    lookups = text.split()
    lookups = [upper_name(s) for s in lookups]  # convert names to upper-first form
    draw_names(canvas, names, lookups)


def handle_search(search_entry, search_out, names):
    """
    (provided) Called for <return> key in lower search field.
    Calls babynames.search() and displays results in GUI.
    Gets search target from given search_entry, puts results
    in given search_out text area.
    """

    target = search_entry.get().strip()
    search_out.delete('1.0', tkinter.END)
    # GUI detail: by deleting always, but only putting in new text
    # if there is data .. hitting return on an empty field
    # lets the user clear the output.
    if target:
        # Call the search_names function in babynames.py
        result = babynames.search_names(names, target)
        out = ' '.join(result)
        search_out.insert('1.0', out)


# main() code is provided
def main():
    args = sys.argv[1:]
    # Establish size - user can override
    width = 1000
    height = 600
    # Let command line override size of window
    if len(args) == 2:
        width = int(args[0])
        height = int(args[1])

    # Load data
    names = babynames.read_files(FILENAMES)

    # Make window
    top = tkinter.Tk()
    top.wm_title('Baby Names')
    canvas = make_gui(top, width, height, names)

    # draw_fixed once at startup so we have the lines
    # even before the user types anything.
    draw_fixed(canvas)

    # This needs to be called just once
    top.mainloop()


if __name__ == '__main__':
    main()
