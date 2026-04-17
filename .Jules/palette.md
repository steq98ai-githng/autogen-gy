## 2026-04-15 - Dynamic aria-label for expanding/collapsing sidebars
**Learning:** Found an accessibility opportunity in the main sidebar toggle buttons where the action is icon-only and changes state (open/close). Screen readers couldn't identify the current state or action.
**Action:** Always verify stateful toggle buttons have dynamic `aria-label` attributes that reflect the upcoming action based on the current state (e.g. `isExpanded ? 'Close' : 'Open'`).

## 2026-04-16 - Dynamic aria-label for stateful utility buttons
**Learning:** Found an accessibility opportunity in the main content header where utility buttons like the Dark Mode Toggle were icon-only and lacked screen reader context for their current state and action. Furthermore, they missed keyboard navigation focus styles, making it hard for keyboard users to track their location.
**Action:** Always verify that utility and stateful buttons have dynamic `aria-label` attributes that reflect the upcoming action based on the current state (e.g. `darkMode === "dark" ? "Switch to light mode" : "Switch to dark mode"`), include `title` tags for hover contexts, and implement clear focus states (`focus:outline-none focus:ring-2 focus:ring-accent`).
