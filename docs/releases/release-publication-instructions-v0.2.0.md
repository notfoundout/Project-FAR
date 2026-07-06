# Project FAR v0.2.0 Release Publication Instructions

Status: Manual publication instructions for environments without GitHub Release permissions.

## Context

The automated environment did not provide a configured Git remote or authenticated GitHub release permission. Publish the GitHub Release manually after the v0.2.0 finalization PR is merged into the latest `main` branch.

## Release Values

- Tag: `v0.2.0`
- Title: `Project FAR v0.2.0`
- Target: latest `main` after the finalization PR is merged
- Body source: `docs/releases/github-release-v0.2.0.md`

## GitHub Web Steps

1. Open the Project FAR repository on GitHub.
2. Open **Releases**.
3. Select **Draft a new release**.
4. In **Choose a tag**, enter `v0.2.0`.
5. If the tag does not already exist, choose to create the tag from the latest `main` branch after the finalization PR has merged.
6. Set **Target** to the latest `main` branch commit that includes the finalization PR.
7. Set **Release title** to `Project FAR v0.2.0`.
8. Open `docs/releases/github-release-v0.2.0.md` from the merged `main` branch.
9. Copy the full contents of `docs/releases/github-release-v0.2.0.md` into the release description.
10. Verify that the release description was copied from the file and was not rewritten from scratch.
11. Publish the release.
12. Confirm that the repository releases page shows `v0.2.0` with title `Project FAR v0.2.0`.

## GitHub Mobile Web Steps

1. Open the Project FAR repository in a mobile browser.
2. Use the repository menu to open **Releases**.
3. Tap **Draft a new release**.
4. Enter or create tag `v0.2.0` from the latest `main` branch after the finalization PR has merged.
5. Enter release title `Project FAR v0.2.0`.
6. Open `docs/releases/github-release-v0.2.0.md` in another browser tab from the merged `main` branch.
7. Copy the full file contents into the release description.
8. Publish the release.
9. Reopen the releases page and confirm that `v0.2.0` is visible.

## Verification

After publication, verify:

- the tag is exactly `v0.2.0`;
- the title is exactly `Project FAR v0.2.0`;
- the target commit is on `main` after the finalization PR merge;
- the body matches `docs/releases/github-release-v0.2.0.md`.
