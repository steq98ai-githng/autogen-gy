## 2026-04-15 - Dynamic aria-label for expanding/collapsing sidebars
**Learning:** Found an accessibility opportunity in the main sidebar toggle buttons where the action is icon-only and changes state (open/close). Screen readers couldn't identify the current state or action.
**Action:** Always verify stateful toggle buttons have dynamic `aria-label` attributes that reflect the upcoming action based on the current state (e.g. `isExpanded ? 'Close' : 'Open'`).
## 2024-03-24 - Accessible Icon-Only Toolbar Buttons
**Learning:** Icon-only buttons (like the dark mode toggle in content header) can be problematic for both cognitive accessibility and screen readers if not handled properly. Adding only tooltips improves visual context, but without ARIA labels, screen readers still miss the button's purpose. Additionally, focus outlines on custom buttons are frequently stripped out, leading to broken keyboard navigation.
**Action:** When adding or auditing icon-only buttons, consistently wrap them in `Tooltip` for visual clarity, add `aria-label` with descriptive text depending on state, and ensure `focus-visible:ring-2` (and corresponding classes) are applied to restore keyboard accessibility indicators.
## 2026-04-17 - [Missing Accessibility on Standalone Utility Icon Buttons]
**Learning:** In Autogen Studio, standalone utility icon buttons (like Dark Mode toggle, Mobile Menu, and User Profile Menu) frequently lack semantic `aria-label`, `title` tooltips, and distinct focus states for keyboard navigation. This compromises accessibility and makes these controls difficult to discern for screen readers and power users.
**Action:** When working on navigation bars or generic headers, always verify that every icon-only button contains explicit `aria-label`/`title` tags and apply global focus visibility utilities such as `focus:outline-none focus-visible:ring-2 focus-visible:ring-accent` for uniform keyboard accessibility.
## 2024-04-19 - Missing ARIA Labels Inside Tooltip Components
**Learning:** In the AutoGen Studio frontend, wrapping an icon-only `<button>` inside an antd `<Tooltip>` component does not automatically provide an accessible name to the inner interactive element. Screen readers would encounter these buttons as completely unlabelled despite the visual tooltip.
**Action:** Always ensure that an `aria-label` is applied directly to the innermost interactive element (e.g. the `<button>`) even when wrapped in a `<Tooltip>` to maintain strict accessibility standards. For dynamic elements like sidebars, use context variables in the aria-label (e.g., `aria-label={\`Teams (${teams.length})\`}`) to provide richer context.
## 2026-04-21 - [Added Accessibility to Chat Input Buttons]
**Learning:** The chat input view lacked proper accessibility and keyboard focus indicators for the 'Upload File' and 'Send message' buttons, which could be frustrating for keyboard-only or screen reader users navigating the main interactive component.
**Action:** Always ensure critical interactive elements in forms/inputs have clear `aria-label` attributes and explicitly utilize `focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent` to provide distinct visual feedback during keyboard navigation.
## 2024-04-20 - Missing ARIA Labels and Focus Rings on Interactive Chat Controls
**Learning:** In the AutoGen Studio playground, numerous interactive icon-only elements (like the replay speed dropdown triggers and upload file button) lacked `aria-label`s, rendering them functionally invisible to screen readers. Furthermore, virtually all control buttons (start replay, cancel run, expand tool calls, flow graph toggles) lacked visible focus rings, severely hindering keyboard-only navigation within the chat interface.
**Action:** When auditing chat or complex interaction views, explicitly test tab navigation. Ensure every actionable element has both a semantic label (`aria-label` or `title`) if it relies on icons, and an active `focus-visible:ring-2` (or equivalent Tailwind class) applied to it.

## 2026-04-21 - [Accessible Diagram Nodes]
**Learning:** Diagram/graph views often use compact, icon-only nodes where the interactive elements lack context. Using dynamic ARIA labels (e.g., incorporating the specific node's label) combined with visual tooltips and focus indicators significantly improves accessibility and clarity for both screen reader and sighted keyboard users.
**Action:** Always wrap icon-only buttons inside node diagrams with `<Tooltip>`, apply dynamic `aria-label` attributes, and ensure `focus-visible` utility classes are present.
## 2023-10-27 - Sidebar Icon-Only Link Accessibility
**Learning:** When building collapsible sidebars where navigation items become icon-only, wrapping the routing component (`<Link>`) in an antd `<Tooltip>` (via an intermediary `<div>` or otherwise) does not reliably transfer an accessible name to the focusable inner element. Screen readers and keyboard users may still encounter generic links without context.
**Action:** Always apply the `aria-label` attribute directly to the interactive component (e.g., the `<Link>`), and ensure there is a clear visual focus indicator (like `focus-visible:ring-2`) directly on the element itself rather than relying entirely on tooltip hover states.
                                              
## 2024-04-27 - Fully associating visible text labels with custom inputs
**Learning:** Found instances where custom UI controls (like styled toggles or number inputs) had descriptive text placed nearby visually, but without semantic connection (missing `htmlFor` on the `<label>` and/or `id` on the `<input>`). This disconnect means the labels are not announced properly by screen readers, and clicking the text does not focus or toggle the control, creating a frustrating experience, especially on mobile or for users with motor impairments.
**Action:** Always ensure any `<label>` text conceptually tied to an input is formally linked via `htmlFor` corresponding to the input's `id`. Additionally, adding `cursor-pointer` to the label text provides visual feedback that the label is an active click target.
## 2026-04-27 - [Forms Label Linking]
**Learning:** Wrapping inputs with <label> tags is insufficient for screen readers if htmlFor and id are not explicitly defined, especially for custom UI controls like toggles.
**Action:** Always link the label using htmlFor pointing to the input id, even when wrapping.

## 2026-04-29 - [Added Keyboard Focus to Interactive Utility Buttons]
**Learning:** In Autogen Studio, custom utility buttons like truncate expansion arrows and fullscreen modal triggers frequently lack visual focus indicators. This makes keyboard navigation difficult or impossible for non-mouse users.
**Action:** When adding custom interactive buttons (e.g. icon-only utility toggles), always explicitly add Tailwind focus utilities such as `focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent` to ensure they are fully navigable by keyboard.

## 2024-05-10 - Sidebar Keyboard Accessibility
**Learning:** In Autogen Studio, the main sidebars and various inner navigation sidebars have icon-only buttons for toggling visibility. While they have `aria-label`s, their focus indicator classes (`focus:ring-2`) were missing the `focus-visible:` prefix. This causes them to show an outline even when clicked with a mouse, which designers often dislike, or they lack visual focus entirely for keyboard users.
**Action:** Always verify that interactive buttons use `focus-visible:` modifiers (e.g., `focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent`) instead of `focus:` to ensure keyboard-only navigation is visually supported while maintaining a clean experience for mouse users.

## 2024-05-02 - Icon-only Button Accessibility in Toolbars
**Learning:** In `autogen-studio` toolbars (like the Team Builder), `Tooltip` components are often used to wrap icon-only `Button`s to provide visual context on hover. However, these `Tooltip`s do not automatically propagate accessible names to the underlying `<button>` elements, leaving them completely unannounced by screen readers. Furthermore, interactive toolbar buttons often lack visible focus indicators for keyboard users.
**Action:** Always verify that icon-only buttons have an explicit `aria-label` directly on the `<Button>` component, even if they are wrapped in a `<Tooltip>`. Additionally, ensure interactive elements receive keyboard focus indicators (e.g., using Tailwind's `focus:outline-none focus-visible:ring-2 focus-visible:ring-accent`).
