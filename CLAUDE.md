# Claude Repository Instructions

Read [AUTHORITY.md](AUTHORITY.md) before using anything here; this file adds one working rule and overrides none of it.

## Links that work: READMEs and pull request descriptions are usable, not reference lists (added 2026-11-01, Chad)

Chad, 2026-11-01: "this is how I want the READMEs and descriptions done in the future: properly usable, not just lists of references." He opens a pull request or a README to get to the work. A path in backticks is a reference he has to go and find; a link takes him there. Every document that points at work must let him click straight through to it.

**Pull request descriptions**

1. Open with `## Start here`, above every template section. Group by project; under each project, the repository files, then the Notion pages.
2. One link per line: `- [Plain name](URL): what it holds, in a few words`. A plain name, not a filename. No strings of links joined by `·`.
3. Link every deliverable a reader would open: each new or substantially changed document, each Notion page or database created or edited. Generated files, manifests and tooling need a link only if they are worth reading.
4. Repository links are full GitHub URLs pinned to the pushed commit's short hash: `https://github.com/CFhacky/the-new-path-engine/blob/<7-character hash>/<path>`. Not the branch name: it makes the URL longer, and the link dies when the branch is deleted after merge. When you push again, update the hash.
5. Keep every URL under 149 characters. The tool path that saves pull request descriptions wraps longer URLs in backticks, which breaks them (found on CFhacky/campaign-development-vault#356). If a file's URL is too long, link its folder (`/tree/<hash>/<folder>`) and name the file.
6. After saving, read the description back. Confirm that no URL is wrapped in backticks and that every repository link names a file that exists at that commit (`git cat-file -e <hash>:<path>`). A description with a broken link is not finished.
7. Template sections follow `## Start here`. Never tick a box whose text is false; write the fact as a sentence instead.

**READMEs**

1. The read order is a numbered list of links, not backticked paths: `1. [Register](REGISTER.md): every artifact, every form, the Notion build.` Use relative links, which work on any branch and after merge.
2. Every file a reader would open is linked from the README, with one line on what it holds.
3. Notion pages the project wrote or depends on are linked by URL under their own titles.
4. Keep backticks for code, commands, branch names and paths that do not exist yet. Never use them to point at work a reader should open.
5. When the work changes, the README changes with it. A README that describes a superseded state is a broken link.

**Notion pages** link the pages and repository files they depend on; never name them in plain text alone.

The model to copy: the `## Start here` section of CFhacky/campaign-development-vault#356, and the READMEs under `projects/in-progress/` in CFhacky/campaign-development-vault.
