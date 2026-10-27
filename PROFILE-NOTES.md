# Profile maintenance

The profile uses a dark mint, blue, and violet visual system with an illustrated hero, animated typing, project cards, technology icons, and visible activity charts. GitHub controls the surrounding page theme.

## Local artwork

Run `python scripts/generate_profile_assets.py` to rebuild the 13 SVG assets using only Python's standard library. The existing doodle PNG is embedded unchanged in both hero variants so the SVGs do not depend on external image requests. It is a symbolic inventor character, not a photographic likeness.

`hero-mobile.svg` and `build-flow-mobile.svg` are selected through native HTML `picture` sources at viewport widths of 640 px and below. Project and stats cards use inline 390 px images that wrap into one column on narrow screens; GitHub limits image width to the available space. No layout tables, JavaScript, iframe, or external font is required.

All local animation uses SVG/CSS and respects `prefers-reduced-motion`. Static defaults leave the hero and first typing message visible if animation is unavailable. The build-flow animation is decorative; it does not represent GitHub activity.

## Dynamic images and fallbacks

- `scripts/update_activity.py` generates the activity, stats, and primary-language cards directly from GitHub's GraphQL API. The dated source is saved in `assets/github-data.json`. Contribution counts follow GitHub's rolling calendar; repositories and stars count owned public non-forks. Language counts describe repository contents, not proficiency.
- `.github/workflows/refresh-profile.yml` refreshes the cards daily at 00:17 UTC (05:17 in Pakistan), on relevant script/workflow changes to `main`, or by manual dispatch. It uses the repository's ephemeral GitHub token, a SHA-pinned official checkout action, and a bot-authored commit. No additional secret or external stats host is needed. It starts after this PR is merged. API failures preserve the last successful cards and surface as a failed workflow run; timestamps and native GitHub links remain available.
- The former third-party summary cards were removed after their contribution and repository counts disagreed with GitHub's API during verification.
- [Skill Icons](https://github.com/tandpfun/skill-icons) provides the three technology-icon rows. Each row has alt text and a visible text equivalent.
- Shields.io provides the three AI focus badges. The same focus appears in ordinary text above.

Essential identity, experience, contact links, and skill names remain accessible through text or descriptive image alternatives. The public workbench describes templates and experiments separately from professional experience. No unsupported metrics, certifications, current employer changes, or framework claims were introduced.

The unused `build-loop.svg` from the first design is retained for historical reuse. The avatar PNG remains available independently for manual account-avatar upload. This README change does not change GitHub account settings.
