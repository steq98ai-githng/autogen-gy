## 2026-04-15 - Dynamic aria-label for expanding/collapsing sidebars
**Learning:** Found an accessibility opportunity in the main sidebar toggle buttons where the action is icon-only and changes state (open/close). Screen readers couldn't identify the current state or action.
**Action:** Always verify stateful toggle buttons have dynamic `aria-label` attributes that reflect the upcoming action based on the current state (e.g. `isExpanded ? 'Close' : 'Open'`).
## 2026-04-17 - [Missing Accessibility on Standalone Utility Icon Buttons]
**Learning:** In Autogen Studio, standalone utility icon buttons (like Dark Mode toggle, Mobile Menu, and User Profile Menu) frequently lack semantic `aria-label`, `title` tooltips, and distinct focus states for keyboard navigation. This compromises accessibility and makes these controls difficult to discern for screen readers and power users.
**Action:** When working on navigation bars or generic headers, always verify that every icon-only button contains explicit `aria-label`/`title` tags and apply global focus visibility utilities such as `focus:outline-none focus-visible:ring-2 focus-visible:ring-accent` for uniform keyboard accessibility.
