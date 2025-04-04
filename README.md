## Getting Started

### Dependencies

Install all dependencies for javascript and Python:

```bash
pnpm install-reqs
```

Or install javascript dependencies only:

```bash
pnpm install
```

Or install dependencies for Python only. Be sure to run with admin privileges. Recommend creating a virtual env:

```
pip install -r requirements.txt
```

Tauri requires icons in the appropriate folder. Run the script to automatically generate icons from a source image. I have included icons for convenience.

```bash
pnpm build:icons
```

### Run

Run the app in development mode:

```bash
pnpm tauri dev
```

## Deploy using your machine

### 1. Compile Python sidecar

Run this at least once before running `pnpm tauri dev` or `pnpm tauri build` and each time you make changes to your python code:

```bash
pnpm build:sidecar-winos
# OR
pnpm build:sidecar-macos
# OR
pnpm build:sidecar-linux
```

In case you dont have PyInstaller installed run:

```
pip install -U pyinstaller
```

A note on compiling Python exe (the -F flag bundles everything into one .exe). You won't need to run this manually each build, I have included it in the build scripts.

### 2. Build Next.js (optional)

Build the static html files that tauri will serve as your front-end.

```bash
pnpm run build
```

### 3. Build tauri (and Next.js)

Tauri will run the "build" script (which does the same as the previous step) before it builds the tauri app, see `tauri.conf.json` file. You can edit what script it runs in the `beforeBuildCommand`.
Build the production app on your machine for a specific OS:

```bash
pnpm tauri build
```

This creates an installer located here:

- `<project-dir>\src-tauri\target\release\bundle\nsis`

And the raw executable here:

- `<project-dir>\src-tauri\target\release`

## Deploy using Github Actions

Fork this repo in order to access a manual trigger to build for each platform (Windows, MacOS, Linux) and upload a release.

You can then modify the `release.yml` file to suit your specific app's build pipeline needs. Workflow permissions must be set to "Read and write". Any git tags created before a workflow existed will not be usable for that workflow. You must specify a tag to run from (not a branch name).

Initiate the Workflow Manually:

1. Navigate to the "Actions" tab in your GitHub repository.
2. Select the "Manual Tauri Release" workflow.
3. Click on "Run workflow" and provide the necessary inputs:

   - release_name: The title of the release.
   - release_notes (optional): Notes or changelog for the release.
   - release_type: ("draft", "public", "private")

## Learn More

- [Tauri Framework](https://tauri.app/) - learn about native app development in javascript and rust.
- [NextJS](https://nextjs.org/docs) - learn about the popular react framework Next.js
- [FastAPI](https://fastapi.tiangolo.com/) - learn about FastAPI server features and API.
- [PyInstaller](https://pyinstaller.org/en/stable/) - learn about packaging python code.
