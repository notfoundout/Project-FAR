#!/usr/bin/env python3
"""Export authenticated review metadata for every merged pull request.

The exporter uses only the GitHub API and Python's standard library. It fails
closed: any API, pagination, mapping, or nested-thread pagination error leaves
``completeness_status`` as ``INCOMPLETE`` and is recorded in the manifest.
No credential or authorization header is written to disk.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

API = "https://api.github.com"
GRAPHQL = f"{API}/graphql"
API_VERSION = "2022-11-28"


@dataclass
class Retrieval:
    endpoint: str
    pr_number: int | None = None
    pages: int = 0
    items: int = 0
    complete: bool = True
    errors: list[str] = field(default_factory=list)

    def as_dict(self) -> dict[str, Any]:
        return {
            "endpoint": self.endpoint,
            "pr_number": self.pr_number,
            "pages": self.pages,
            "items": self.items,
            "complete": self.complete,
            "errors": self.errors,
        }


class GitHubClient:
    def __init__(self, token: str, repository: str) -> None:
        if not token:
            raise ValueError("a GitHub token is required")
        if repository.count("/") != 1:
            raise ValueError("repository must be owner/name")
        self.token = token
        self.repository = repository
        self.owner, self.name = repository.split("/", 1)

    def _request(self, url: str, *, payload: dict[str, Any] | None = None) -> tuple[Any, dict[str, str]]:
        data = None
        method = "GET"
        if payload is not None:
            data = json.dumps(payload).encode("utf-8")
            method = "POST"
        request = urllib.request.Request(
            url,
            data=data,
            method=method,
            headers={
                "Accept": "application/vnd.github+json",
                "Authorization": f"Bearer {self.token}",
                "X-GitHub-Api-Version": API_VERSION,
                "User-Agent": "project-far-review-inventory-exporter",
                "Content-Type": "application/json",
            },
        )
        try:
            with urllib.request.urlopen(request, timeout=60) as response:
                raw = response.read().decode("utf-8")
                headers = {key.lower(): value for key, value in response.headers.items()}
                return (json.loads(raw) if raw else None), headers
        except urllib.error.HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"HTTP {exc.code} for {url}: {body[:1000]}") from exc
        except urllib.error.URLError as exc:
            raise RuntimeError(f"request failed for {url}: {exc}") from exc

    def rest_pages(self, path: str, retrieval: Retrieval) -> list[dict[str, Any]]:
        separator = "&" if "?" in path else "?"
        url = f"{API}{path}{separator}per_page=100"
        results: list[dict[str, Any]] = []
        visited: set[str] = set()
        while url:
            if url in visited:
                retrieval.complete = False
                retrieval.errors.append(f"pagination loop detected at {url}")
                break
            visited.add(url)
            try:
                payload, headers = self._request(url)
            except Exception as exc:  # fail-closed accounting
                retrieval.complete = False
                retrieval.errors.append(str(exc))
                break
            retrieval.pages += 1
            if not isinstance(payload, list):
                retrieval.complete = False
                retrieval.errors.append(f"expected list response from {url}")
                break
            results.extend(payload)
            retrieval.items += len(payload)
            url = parse_next_link(headers.get("link", ""))
        return results

    def graphql(self, query: str, variables: dict[str, Any]) -> dict[str, Any]:
        payload, _ = self._request(GRAPHQL, payload={"query": query, "variables": variables})
        if not isinstance(payload, dict):
            raise RuntimeError("GraphQL response was not an object")
        if payload.get("errors"):
            raise RuntimeError(f"GraphQL errors: {json.dumps(payload['errors'], sort_keys=True)}")
        data = payload.get("data")
        if not isinstance(data, dict):
            raise RuntimeError("GraphQL response omitted data")
        return data


def parse_next_link(value: str) -> str | None:
    for part in value.split(","):
        section = part.strip()
        if 'rel="next"' not in section:
            continue
        start = section.find("<")
        end = section.find(">", start + 1)
        if start >= 0 and end > start:
            return section[start + 1 : end]
    return None


def keep_user(user: Any) -> dict[str, Any] | None:
    if not isinstance(user, dict):
        return None
    return {
        "login": user.get("login"),
        "id": user.get("id"),
        "type": user.get("type"),
        "html_url": user.get("html_url"),
    }


def normalize_pr(pr: dict[str, Any]) -> dict[str, Any]:
    return {
        "number": pr.get("number"),
        "title": pr.get("title"),
        "html_url": pr.get("html_url"),
        "state": pr.get("state"),
        "draft": pr.get("draft"),
        "user": keep_user(pr.get("user")),
        "base_ref": (pr.get("base") or {}).get("ref"),
        "base_sha": (pr.get("base") or {}).get("sha"),
        "head_ref": (pr.get("head") or {}).get("ref"),
        "head_sha": (pr.get("head") or {}).get("sha"),
        "merge_commit_sha": pr.get("merge_commit_sha"),
        "created_at": pr.get("created_at"),
        "updated_at": pr.get("updated_at"),
        "closed_at": pr.get("closed_at"),
        "merged_at": pr.get("merged_at"),
    }


def normalize_issue_comment(pr_number: int, item: dict[str, Any]) -> dict[str, Any]:
    return {
        "kind": "issue_comment",
        "pr_number": pr_number,
        "id": item.get("id"),
        "node_id": item.get("node_id"),
        "html_url": item.get("html_url"),
        "user": keep_user(item.get("user")),
        "body": item.get("body"),
        "created_at": item.get("created_at"),
        "updated_at": item.get("updated_at"),
        "author_association": item.get("author_association"),
    }


def normalize_review_comment(pr_number: int, item: dict[str, Any]) -> dict[str, Any]:
    return {
        "kind": "inline_review_comment",
        "pr_number": pr_number,
        "id": item.get("id"),
        "node_id": item.get("node_id"),
        "pull_request_review_id": item.get("pull_request_review_id"),
        "in_reply_to_id": item.get("in_reply_to_id"),
        "html_url": item.get("html_url"),
        "user": keep_user(item.get("user")),
        "body": item.get("body"),
        "commit_id": item.get("commit_id"),
        "original_commit_id": item.get("original_commit_id"),
        "path": item.get("path"),
        "line": item.get("line"),
        "side": item.get("side"),
        "start_line": item.get("start_line"),
        "start_side": item.get("start_side"),
        "original_line": item.get("original_line"),
        "original_start_line": item.get("original_start_line"),
        "diff_hunk": item.get("diff_hunk"),
        "created_at": item.get("created_at"),
        "updated_at": item.get("updated_at"),
        "author_association": item.get("author_association"),
    }


def normalize_review(pr_number: int, item: dict[str, Any]) -> dict[str, Any]:
    return {
        "pr_number": pr_number,
        "id": item.get("id"),
        "node_id": item.get("node_id"),
        "html_url": item.get("html_url"),
        "user": keep_user(item.get("user")),
        "body": item.get("body"),
        "state": item.get("state"),
        "commit_id": item.get("commit_id"),
        "submitted_at": item.get("submitted_at"),
        "author_association": item.get("author_association"),
    }


THREAD_QUERY = """
query($owner:String!, $name:String!, $number:Int!, $after:String) {
  repository(owner:$owner, name:$name) {
    pullRequest(number:$number) {
      id
      reviewThreads(first:100, after:$after) {
        pageInfo { hasNextPage endCursor }
        nodes {
          id isResolved isOutdated path line startLine diffSide
          originalLine originalStartLine
          resolvedBy { login }
          comments(first:100) {
            pageInfo { hasNextPage endCursor }
            nodes {
              id databaseId url body createdAt updatedAt
              author { login }
              replyTo { id databaseId }
              pullRequestReview { id databaseId state submittedAt }
            }
          }
        }
      }
    }
  }
}
"""

THREAD_COMMENTS_QUERY = """
query($id:ID!, $after:String) {
  node(id:$id) {
    ... on PullRequestReviewThread {
      comments(first:100, after:$after) {
        pageInfo { hasNextPage endCursor }
        nodes {
          id databaseId url body createdAt updatedAt
          author { login }
          replyTo { id databaseId }
          pullRequestReview { id databaseId state submittedAt }
        }
      }
    }
  }
}
"""


def fetch_threads(client: GitHubClient, pr_number: int, retrieval: Retrieval) -> list[dict[str, Any]]:
    threads: list[dict[str, Any]] = []
    after: str | None = None
    seen_cursors: set[str | None] = set()
    while True:
        if after in seen_cursors:
            retrieval.complete = False
            retrieval.errors.append(f"thread cursor loop for PR #{pr_number}: {after}")
            break
        seen_cursors.add(after)
        try:
            data = client.graphql(
                THREAD_QUERY,
                {"owner": client.owner, "name": client.name, "number": pr_number, "after": after},
            )
        except Exception as exc:
            retrieval.complete = False
            retrieval.errors.append(str(exc))
            break
        retrieval.pages += 1
        pull = ((data.get("repository") or {}).get("pullRequest"))
        if not isinstance(pull, dict):
            retrieval.complete = False
            retrieval.errors.append(f"PR #{pr_number} missing from GraphQL response")
            break
        connection = pull.get("reviewThreads") or {}
        nodes = connection.get("nodes") or []
        for node in nodes:
            comments_connection = node.get("comments") or {}
            comments = list(comments_connection.get("nodes") or [])
            comment_page_info = comments_connection.get("pageInfo") or {}
            comment_after = comment_page_info.get("endCursor")
            while comment_page_info.get("hasNextPage"):
                try:
                    extra = client.graphql(THREAD_COMMENTS_QUERY, {"id": node.get("id"), "after": comment_after})
                except Exception as exc:
                    retrieval.complete = False
                    retrieval.errors.append(f"thread {node.get('id')} comments: {exc}")
                    break
                retrieval.pages += 1
                extra_connection = ((extra.get("node") or {}).get("comments") or {})
                comments.extend(extra_connection.get("nodes") or [])
                next_info = extra_connection.get("pageInfo") or {}
                next_cursor = next_info.get("endCursor")
                if next_info.get("hasNextPage") and next_cursor == comment_after:
                    retrieval.complete = False
                    retrieval.errors.append(f"comment cursor loop in thread {node.get('id')}")
                    break
                comment_after = next_cursor
                comment_page_info = next_info
            threads.append(
                {
                    "pr_number": pr_number,
                    "id": node.get("id"),
                    "is_resolved": node.get("isResolved"),
                    "is_outdated": node.get("isOutdated"),
                    "path": node.get("path"),
                    "line": node.get("line"),
                    "start_line": node.get("startLine"),
                    "diff_side": node.get("diffSide"),
                    "original_line": node.get("originalLine"),
                    "original_start_line": node.get("originalStartLine"),
                    "resolved_by": (node.get("resolvedBy") or {}).get("login"),
                    "comments": comments,
                }
            )
        retrieval.items += len(nodes)
        page_info = connection.get("pageInfo") or {}
        if not page_info.get("hasNextPage"):
            break
        next_after = page_info.get("endCursor")
        if not next_after:
            retrieval.complete = False
            retrieval.errors.append(f"PR #{pr_number} reports next thread page without cursor")
            break
        after = next_after
    return threads


def write_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")


def unique_non_null(items: Iterable[dict[str, Any]], key: str) -> tuple[bool, list[Any]]:
    seen: set[Any] = set()
    duplicates: list[Any] = []
    for item in items:
        value = item.get(key)
        if value is None:
            duplicates.append(None)
        elif value in seen:
            duplicates.append(value)
        else:
            seen.add(value)
    return not duplicates, duplicates


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repository", default=os.environ.get("GITHUB_REPOSITORY"))
    parser.add_argument("--token", default=os.environ.get("GITHUB_TOKEN"))
    parser.add_argument("--audited-sha", default=os.environ.get("GITHUB_SHA"))
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    if not args.repository or not args.token or not args.audited_sha:
        parser.error("repository, token, and audited SHA are required")

    output: Path = args.output
    output.mkdir(parents=True, exist_ok=True)
    client = GitHubClient(args.token, args.repository)
    retrievals: list[Retrieval] = []
    started = datetime.now(timezone.utc).isoformat()

    pr_retrieval = Retrieval(endpoint="GET /repos/{owner}/{repo}/pulls?state=closed")
    retrievals.append(pr_retrieval)
    closed_prs = client.rest_pages(
        f"/repos/{client.owner}/{client.name}/pulls?state=closed&sort=created&direction=asc",
        pr_retrieval,
    )
    merged = [normalize_pr(pr) for pr in closed_prs if pr.get("merged_at")]
    merged.sort(key=lambda item: int(item["number"]))

    all_comments: list[dict[str, Any]] = []
    all_reviews: list[dict[str, Any]] = []
    all_threads: list[dict[str, Any]] = []

    for index, pr in enumerate(merged, 1):
        number = int(pr["number"])
        print(f"[{index}/{len(merged)}] exporting PR #{number}", flush=True)

        issue_retrieval = Retrieval(endpoint="GET /repos/{owner}/{repo}/issues/{pr}/comments", pr_number=number)
        retrievals.append(issue_retrieval)
        issue_comments = client.rest_pages(
            f"/repos/{client.owner}/{client.name}/issues/{number}/comments", issue_retrieval
        )
        all_comments.extend(normalize_issue_comment(number, item) for item in issue_comments)

        review_retrieval = Retrieval(endpoint="GET /repos/{owner}/{repo}/pulls/{pr}/reviews", pr_number=number)
        retrievals.append(review_retrieval)
        reviews = client.rest_pages(
            f"/repos/{client.owner}/{client.name}/pulls/{number}/reviews", review_retrieval
        )
        all_reviews.extend(normalize_review(number, item) for item in reviews)

        inline_retrieval = Retrieval(endpoint="GET /repos/{owner}/{repo}/pulls/{pr}/comments", pr_number=number)
        retrievals.append(inline_retrieval)
        inline_comments = client.rest_pages(
            f"/repos/{client.owner}/{client.name}/pulls/{number}/comments", inline_retrieval
        )
        all_comments.extend(normalize_review_comment(number, item) for item in inline_comments)

        thread_retrieval = Retrieval(endpoint="GraphQL pullRequest.reviewThreads", pr_number=number)
        retrievals.append(thread_retrieval)
        all_threads.extend(fetch_threads(client, number, thread_retrieval))

        # Avoid secondary-rate-limit bursts while remaining deterministic.
        time.sleep(0.05)

    pr_numbers = {int(item["number"]) for item in merged}
    mapping_errors: list[str] = []
    for collection_name, collection in (
        ("comments", all_comments),
        ("reviews", all_reviews),
        ("threads", all_threads),
    ):
        bad = sorted({item.get("pr_number") for item in collection if item.get("pr_number") not in pr_numbers})
        if bad:
            mapping_errors.append(f"{collection_name} reference unknown PRs: {bad}")

    uniqueness_checks: dict[str, Any] = {}
    for name, collection, key in (
        ("pull_requests", merged, "number"),
        ("review_comments", [x for x in all_comments if x["kind"] == "inline_review_comment"], "id"),
        ("issue_comments", [x for x in all_comments if x["kind"] == "issue_comment"], "id"),
        ("reviews", all_reviews, "id"),
        ("threads", all_threads, "id"),
    ):
        ok, duplicates = unique_non_null(collection, key)
        uniqueness_checks[name] = {"ok": ok, "duplicates_or_nulls": duplicates}

    reply_ids = {
        item["id"]
        for item in all_comments
        if item["kind"] == "inline_review_comment" and item.get("id") is not None
    }
    bad_replies = sorted(
        {
            item["in_reply_to_id"]
            for item in all_comments
            if item["kind"] == "inline_review_comment"
            and item.get("in_reply_to_id") is not None
            and item["in_reply_to_id"] not in reply_ids
        }
    )

    complete = (
        all(item.complete for item in retrievals)
        and not mapping_errors
        and all(value["ok"] for value in uniqueness_checks.values())
        and not bad_replies
    )
    status = "COMPLETE" if complete else "INCOMPLETE"

    counts = {
        "merged_pull_requests": len(merged),
        "issue_comments": sum(item["kind"] == "issue_comment" for item in all_comments),
        "inline_review_comments": sum(item["kind"] == "inline_review_comment" for item in all_comments),
        "review_submissions": len(all_reviews),
        "review_threads": len(all_threads),
    }
    manifest = {
        "schema_version": 2,
        "repository": args.repository,
        "audited_sha": args.audited_sha,
        "started_at": started,
        "completed_at": datetime.now(timezone.utc).isoformat(),
        "authentication": "GitHub Actions GITHUB_TOKEN (credential not persisted)",
        "completeness_status": status,
        "counts": counts,
        "retrievals": [item.as_dict() for item in retrievals],
        "integrity": {
            "mapping_errors": mapping_errors,
            "uniqueness_checks": uniqueness_checks,
            "invalid_reply_parent_ids": bad_replies,
        },
    }

    write_json(output / "raw-pr-inventory.json", {"schema_version": 2, "pull_requests": merged})
    write_json(output / "raw-review-comments.json", {"schema_version": 2, "comments": all_comments})
    write_json(output / "raw-review-submissions.json", {"schema_version": 2, "reviews": all_reviews})
    write_json(output / "raw-review-threads.json", {"schema_version": 2, "threads": all_threads})
    write_json(output / "retrieval-manifest.json", manifest)

    summary = [
        "# Authenticated merged-PR review inventory",
        "",
        f"- Repository: `{args.repository}`",
        f"- Audited SHA: `{args.audited_sha}`",
        f"- Completeness: **{status}**",
        f"- Merged pull requests: {counts['merged_pull_requests']}",
        f"- Issue comments: {counts['issue_comments']}",
        f"- Review submissions: {counts['review_submissions']}",
        f"- Inline review comments: {counts['inline_review_comments']}",
        f"- Review threads: {counts['review_threads']}",
        "",
        "The token used for retrieval was not persisted. See `retrieval-manifest.json` for endpoint-level pagination and integrity accounting.",
        "",
    ]
    (output / "inventory-summary.md").write_text("\n".join(summary), encoding="utf-8")

    limitations = ["# Retrieval limitations", ""]
    failures = [item for item in retrievals if not item.complete]
    if failures or mapping_errors or bad_replies or not all(v["ok"] for v in uniqueness_checks.values()):
        limitations.append("The inventory is incomplete for the following fail-closed reasons:")
        limitations.append("")
        for item in failures:
            limitations.append(f"- `{item.endpoint}` PR `{item.pr_number}`: {'; '.join(item.errors)}")
        for error in mapping_errors:
            limitations.append(f"- {error}")
        if bad_replies:
            limitations.append(f"- Missing inline reply parents: {bad_replies}")
        for name, value in uniqueness_checks.items():
            if not value["ok"]:
                limitations.append(f"- `{name}` duplicate or null identifiers: {value['duplicates_or_nulls']}")
    else:
        limitations.append("No retrieval or pagination limitation was detected by the exporter.")
    limitations.append("")
    (output / "retrieval-limitations.md").write_text("\n".join(limitations), encoding="utf-8")

    print(json.dumps({"status": status, "counts": counts}, sort_keys=True))
    return 0 if complete else 2


if __name__ == "__main__":
    sys.exit(main())
