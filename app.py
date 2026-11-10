
"""Technician-friendly offline demonstration. All readings are synthetic."""

import tkinter as tk
from tkinter import ttk
from recovery import SCENARIOS, evaluate

REPORTS = {
    'CONTINUE_TO_PRESS': (
        'Bearing pickup completed',
        'READY FOR NEXT OPERATION',
        'The proposed bearing-presence check reports a bearing in the gripper.',
        'The next programmed operation may proceed only after the remaining machine checks pass.',
        '#176b42'
    ),
    'SIMULATED_RETRY_ELIGIBLE': (
        'Bearing pickup unsuccessful',
        'RETRY CONDITIONS MET IN SIMULATION',
        'The bearing is not confirmed in the gripper. The example inputs indicate that it remains at a known pickup location and the required retry conditions are satisfied.',
        'Keep pressing paused. A controlled retry could be requested through a separately validated robot recovery procedure.',
        '#9b5a00'
    ),
    'BLOCK_AND_INSPECT': (
        'Bearing pickup needs attention',
        'OPERATOR INSPECTION REQUIRED',
        'The bearing pickup could not be confirmed, or a condition required for retrying is missing.',
        'Keep the automatic sequence blocked. Inspect the pickup area and follow the approved restart procedure.',
        '#aa2730'
    ),
}

DETAILS = [
    ('tool_ok', 'Correct tool attached (RFID)'),
    ('cylinder_in_pick_position', 'Cylinder in expected position (reed contact)'),
    ('bearing_held', 'Bearing detected in gripper (PROPOSED sensor)'),
    ('bearing_at_known_pick_location', 'Bearing still at known pickup location (assumed)'),
    ('gripper_clear', 'Gripper clear (assumed)'),
    ('cell_clear', 'Cell clear (assumed)'),
    ('operator_approved', 'Operator approval (simulated)'),
    ('retry_count', 'Previous retry attempts'),
]

# --------------------------------------------------
# MAIN WINDOW
# --------------------------------------------------

root = tk.Tk()
root.title('Prefilter | Technician Fault Report — Synthetic Demo')

# Smaller initial window so it fits on most screens.
root.geometry('950x650')
root.minsize(650, 400)

style = ttk.Style()
style.configure('Heading.TLabel', font=('Segoe UI', 19, 'bold'))
style.configure('Section.TLabel', font=('Segoe UI', 11, 'bold'))
style.configure('Body.TLabel', font=('Segoe UI', 10))

# --------------------------------------------------
# SCROLLABLE WINDOW - NEW
# --------------------------------------------------

container = ttk.Frame(root)
container.pack(fill='both', expand=True)

canvas = tk.Canvas(
    container,
    highlightthickness=0,
    borderwidth=0
)
canvas.pack(side='left', fill='both', expand=True)

scrollbar = ttk.Scrollbar(
    container,
    orient='vertical',
    command=canvas.yview
)
scrollbar.pack(side='right', fill='y')

canvas.configure(yscrollcommand=scrollbar.set)

# All existing interface widgets go inside this frame.
frame = ttk.Frame(canvas, padding=22)

canvas_window = canvas.create_window(
    (0, 0),
    window=frame,
    anchor='nw'
)


def update_scroll_region(event=None):
    """Update scrolling whenever content height changes."""
    canvas.configure(scrollregion=canvas.bbox('all'))


def resize_content(event):
    """Keep the content width equal to the visible window width."""
    canvas.itemconfigure(canvas_window, width=event.width)


frame.bind('<Configure>', update_scroll_region)
canvas.bind('<Configure>', resize_content)


def on_mousewheel(event):
    """Enable mouse-wheel scrolling on Windows."""
    canvas.yview_scroll(int(-event.delta / 120), 'units')


canvas.bind_all('<MouseWheel>', on_mousewheel)

# --------------------------------------------------
# HEADER
# --------------------------------------------------

ttk.Label(
    frame,
    text='Prefilter — Bearing Pickup',
    style='Heading.TLabel'
).pack(anchor='w')

ttk.Label(
    frame,
    text='TECHNICIAN VIEW  |  SYNTHETIC INPUTS  |  NOT CONNECTED TO KUKA / PLC',
    foreground='#955200'
).pack(anchor='w', pady=(4, 18))

ttk.Label(
    frame,
    text='Choose an example situation:',
    style='Section.TLabel'
).pack(anchor='w')

choice = tk.StringVar(value='Failed pickup — approved retry')

combo = ttk.Combobox(
    frame,
    state='readonly',
    textvariable=choice,
    values=list(SCENARIOS),
    width=49
)
combo.pack(anchor='w', pady=(6, 16))

# --------------------------------------------------
# TECHNICIAN SUMMARY
# --------------------------------------------------

summary = ttk.LabelFrame(
    frame,
    text='What the technician needs to know',
    padding=16
)
summary.pack(fill='x')

headline = ttk.Label(
    summary,
    font=('Segoe UI', 17, 'bold')
)
headline.pack(anchor='w')

status = ttk.Label(
    summary,
    font=('Segoe UI', 11, 'bold')
)
status.pack(anchor='w', pady=(6, 16))

ttk.Label(
    summary,
    text='What happened, and why?',
    style='Section.TLabel'
).pack(anchor='w')

reason = ttk.Label(
    summary,
    style='Body.TLabel',
    wraplength=800,
    justify='left'
)
reason.pack(anchor='w', fill='x', pady=(4, 14))

ttk.Label(
    summary,
    text='What should happen next?',
    style='Section.TLabel'
).pack(anchor='w')

action = ttk.Label(
    summary,
    style='Body.TLabel',
    wraplength=800,
    justify='left'
)
action.pack(anchor='w', fill='x', pady=(4, 0))

# --------------------------------------------------
# EVENT HISTORY
# --------------------------------------------------

steps = ttk.LabelFrame(
    frame,
    text='Event history — illustrative sequence, not actual PLC events',
    padding=12
)
steps.pack(fill='x', pady=(14, 0))

events = ttk.Label(
    steps,
    wraplength=810,
    justify='left'
)
events.pack(anchor='w')

# --------------------------------------------------
# TECHNICAL DETAILS
# --------------------------------------------------

details_box = ttk.LabelFrame(
    frame,
    text='Technical details (maintenance view)',
    padding=12
)

details_visible = tk.BooleanVar(value=False)

detail_rows = ttk.Frame(details_box)
value_labels = {}

for i, (key, title) in enumerate(DETAILS):

    ttk.Label(
        detail_rows,
        text=title
    ).grid(
        row=i,
        column=0,
        sticky='w',
        padx=(0, 22),
        pady=3
    )

    val = ttk.Label(
        detail_rows,
        font=('Segoe UI', 9, 'bold')
    )

    val.grid(
        row=i,
        column=1,
        sticky='w',
        pady=3
    )

    value_labels[key] = val


def toggle_details():
    if details_visible.get():

        detail_rows.pack_forget()
        details_visible.set(False)

        toggle.config(
            text='Show sensor and PLC details'
        )

    else:

        detail_rows.pack(anchor='w', fill='x')
        details_visible.set(True)

        toggle.config(
            text='Hide sensor and PLC details'
        )

    # NEW: Refresh the scrollbar after expanding/collapsing.
    root.after_idle(update_scroll_region)


toggle = ttk.Button(
    frame,
    text='Show sensor and PLC details',
    command=toggle_details
)
toggle.pack(anchor='w', pady=(14, 4))

details_box.pack(fill='x')

# --------------------------------------------------
# FOOTER
# --------------------------------------------------

footer = ttk.Label(
    frame,
    text=(
        'Concept only: real recovery requires verified sensors, '
        'PLC/safety interlocks, and an approved KUKA robot program.'
    ),
    foreground='#6c5b47',
    wraplength=810
)
footer.pack(anchor='w', pady=(14, 0))

# --------------------------------------------------
# UPDATE REPORT
# --------------------------------------------------

def update(*_):

    signals = SCENARIOS[choice.get()]
    decision, machine_reason = evaluate(signals)

    title, state, why, next_action, color = REPORTS[decision]

    if decision == 'BLOCK_AND_INSPECT':

        if signals.retry_count >= 1:
            why = (
                'The bearing is not confirmed in the gripper, '
                'and the permitted retry limit has been reached.'
            )

        elif not signals.tool_ok or not signals.cylinder_in_pick_position:
            why = (
                'The correct tool or expected cylinder position '
                'is not confirmed. The robot must not proceed.'
            )

        else:
            why = (
                'The bearing is not confirmed in the gripper, '
                'and at least one retry condition cannot be verified '
                '(for example, bearing location or cell clearance).'
            )

    headline.config(text=title)
    status.config(text=state, foreground=color)
    reason.config(text=why)
    action.config(text=next_action)

    history = (
        '1. Robot attempts bearing pickup.\n'
        '2. Proposed bearing-presence check evaluates the result.\n'
    )

    if decision == 'CONTINUE_TO_PRESS':

        history += (
            '3. Bearing presence confirmed.\n'
            '4. Next operation remains subject to normal machine checks.'
        )

    elif decision == 'SIMULATED_RETRY_ELIGIBLE':

        history += (
            '3. Bearing not detected; pressing remains blocked.\n'
            '4. Example retry conditions checked.\n'
            '5. Controlled retry may be requested; '
            'no robot movement is commanded.'
        )

    else:

        history += (
            '3. Pickup cannot be verified; pressing remains blocked.\n'
            '4. Retry not permitted; operator inspection required.'
        )

    events.config(text=history)

    for key, _ in DETAILS:

        value = getattr(signals, key)

        if isinstance(value, int) and not isinstance(value, bool):
            display_value = str(value)
        else:
            display_value = (
                'YES (simulated)'
                if value
                else 'NO / NOT CONFIRMED (simulated)'
            )

        value_labels[key].config(text=display_value)

    # NEW: Update scrolling after changing the report.
    root.after_idle(update_scroll_region)


# --------------------------------------------------
# START APPLICATION
# --------------------------------------------------

choice.trace_add('write', update)
update()

root.mainloop()
