## 2026-04-15 - Dynamic aria-label for expanding/collapsing sidebars
**Learning:** Found an accessibility opportunity in the main sidebar toggle buttons where the action is icon-only and changes state (open/close). Screen readers couldn't identify the current state or action.
**Action:** Always verify stateful toggle buttons have dynamic `aria-label` attributes that reflect the upcoming action based on the current state (e.g. `isExpanded ? 'Close' : 'Open'`).
## 2024-03-24 - Accessible Icon-Only Toolbar Buttons
**Learning:** Icon-only buttons (like the dark mode toggle in content header) can be problematic for both cognitive accessibility and screen readers if not handled properly. Adding only tooltips improves visual context, but without ARIA labels, screen readers still miss the button's purpose. Additionally, focus outlines on custom buttons are frequently stripped out, leading to broken keyboard navigation.
**Action:** When adding or auditing icon-only buttons, consistently wrap them in `Tooltip` for visual clarity, add `aria-label` with descriptive text depending on state, and ensure `focus-visible:ring-2` (and corresponding classes) are applied to restore keyboard accessibility indicators.
## 2026-04-17 - [Missing Accessibility on Standalone Utility Icon Buttons]
**Learning:** In Autogen Studio, standalone utility icon buttons (like Dark Mode toggle, Mobile Menu, and User Profile Menu) frequently lack semantic `aria-label`, `title` tooltips, and distinct focus states for keyboard navigation. This compromises accessibility and makes these controls difficult to discern for screen readers and power users.
**Action:** When working on navigation bars or generic headers, always verify that every icon-only button contains explicit `aria-label`/`title` tags and apply global focus visibility utilities such as `focus:outline-none focus-visible:ring-2 focus-visible:ring-accent` for uniform keyboard accessibility.
## 2024-04-19 - Dynamic aria-labels for list items
**Learning:** Icon-only buttons mapped from a list in React (like edit/delete session buttons in the playground) need context to be accessible. A static label like 'Delete' doesn't help screen reader users know *what* they are deleting.
**Action:** Always use dynamic ARIA labels (e.g., `aria-label={\`Delete ${item.name}\`}`) when adding accessibility to buttons that interact with mapped list items.
