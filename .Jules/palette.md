## 2026-04-15 - Dynamic aria-label for expanding/collapsing sidebars
**Learning:** Found an accessibility opportunity in the main sidebar toggle buttons where the action is icon-only and changes state (open/close). Screen readers couldn't identify the current state or action.
**Action:** Always verify stateful toggle buttons have dynamic `aria-label` attributes that reflect the upcoming action based on the current state (e.g. `isExpanded ? 'Close' : 'Open'`).
