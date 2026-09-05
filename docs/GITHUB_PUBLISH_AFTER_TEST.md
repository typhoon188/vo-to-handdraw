# GitHub publication plan — after local Hermes validation

Recommended public repository layout is already present in this release:

```text
repo-root/
├── README.md
├── HERMES_INSTALL.md
└── skills/
    └── vo-to-handdraw/
        ├── SKILL.md
        ├── handdraw.py
        ├── planner/
        ├── runtime/
        ├── scripts/
        ├── assets/
        ├── examples/
        └── tests/
```

After a public GitHub repo exists, Hermes can install the individual skill with:

```bash
hermes skills install OWNER/REPO/skills/vo-to-handdraw
```

For a reusable skill tap, users can also add the repository as a tap and install from it.

Before publishing publicly, choose a repository license and review the bundled asset/license provenance.
