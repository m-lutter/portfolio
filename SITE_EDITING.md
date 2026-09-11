# Editing the portfolio website

The public site is built from the `docs/` folder and hosted on GitHub Pages.

- `content/projects.mjs`: featured project copy, supporting links, and the eight-circuit archive.
- `scripts/build.mjs`: homepage copy and shared page templates. Uses Node.js built-ins; no packages to install.
- `docs/styles.css`: colors, layout, typography, responsive styles, and print styles.
- `docs/site.js`: accessible featured-project filtering.
- `docs/assets/`: images copied from the original public portfolio.

Run `node scripts/build.mjs` after editing content or templates. Commit both the source and the generated `docs/` files. Run `node scripts/serve.mjs` for a local preview at `http://127.0.0.1:4173/portfolio/`.

GitHub Pages configuration: deploy from branch `main`, folder `/docs`. A `.nojekyll` file makes this a plain static site. There are no runtime dependencies, analytics scripts, API keys, or sign-in requirements.

## Content basis

The initial page uses the public `m-lutter/portfolio` digital-systems collection and the public `m-lutter/orbital-training` README. Orbital is identified as a deployed beta, not a finished stable release. The pump repository contained only a planning skeleton when reviewed and is not featured. Private repository contents are not included.

Digital projects retain distinctions between simulated designs, physical builds, and incomplete extensions. The 75-to-40 gate comparison comes from the original 5421 BCD write-up and is not a power or timing measurement. Original project folders are preserved.

The EPROM and Frogger images were copied from working image attachments in their original README files. The BCD image is the original Tinkercad export. Several original local JPEG/MOV files contain only two bytes; they are not linked as usable media.

The biography reflects the owner's September 2026 Job Research context: UIUC aerospace engineering, expected December 2026 graduation, launch-vehicle systems/integration, and GNC/avionics integration. Update the graduation wording when appropriate. Contact uses the owner's connected GitHub profile email.
