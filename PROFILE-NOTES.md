# Profile maintenance

This README is designed for GitHub's Markdown renderer: native links and disclosure sections, wrapping badges, single-column content, and responsive images. There is no JavaScript or iframe dependency.

## Assets and accessibility

- `assets/hasham-doodle-avatar.png` is an original AI-generated inventor doodle inspired by Hasham's supplied sketch: black ink, a winking face, a crooked cap, and a mint-green flask. It is a symbolic character, not a claim of photographic likeness.
- `assets/build-loop.svg` is a local, self-contained SVG. Its short typing animation stops, respects `prefers-reduced-motion`, and defaults to readable static text without animation support. Its message is repeated in accessible image text.
- All essential identity, experience, skills, and contact information is ordinary text. Badges wrap; there are no fixed-width multi-column tables.

## Dynamic cards

The stats card and contribution timeline use [GitHub Profile Summary Cards](https://github.com/vn7n24fzkq/github-profile-summary-cards). Both are configured for `Hashamjavedofficial`, are fetched as images, and may be cached or temporarily unavailable. Persistent text links to GitHub's overview, repositories, and pull requests provide an alternative. The timeline is expandable to keep the default view concise. The initially considered Activity Graph endpoint returned HTTP 402 during verification, so it is not used.

The six stack badges use Shields.io. The expanded toolbox preserves the same skills as text. No secrets, personal access tokens, or workflow permissions are needed for these cards. GitHub controls the surrounding page theme; the custom illustration, SVG, badges, and cards have explicit dark surfaces.

## Content boundaries

The profile uses Hasham's reported professional experience and explicitly confirmed positioning. Public repositories are presented as a workbench of templates and experiments, not proof of ownership of unrelated professional projects. No unsupported performance figures, certifications, job dates, employer changes, or named AI framework expertise were added.

To publish the redesign, merge the profile pull request into this repository's default branch. Relative asset links work on the review branch and after merging. Changing the account avatar is a separate GitHub settings action.
