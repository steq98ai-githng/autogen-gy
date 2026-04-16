import asyncio
import json
import os
import sqlite3
import subprocess
from contextlib import closing
from typing import Optional

from chromadb import PersistentClient
from chromadb.utils import embedding_functions
from tqdm import tqdm

from ._config import get_gitty_dir
from ._github import get_github_issue_content


def init_db(db_path: str) -> None:
    with closing(sqlite3.connect(db_path)) as conn:
        with conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS issues (
                    number INTEGER PRIMARY KEY,
                    title TEXT,
                    updatedAt TEXT,
                    content TEXT
                )
            """)


def update_issue(db_path: str, number: int, title: str, updatedAt: str, content: str) -> None:
    with closing(sqlite3.connect(db_path)) as conn:
        with conn:
            conn.execute(
                """
                INSERT OR REPLACE INTO issues (number, title, updatedAt, content)
                VALUES (?, ?, ?, ?)
                """,
                (number, title, updatedAt, content),
            )


def update_chroma(gitty_dir: str, db_path: str) -> None:
    persist_directory = os.path.join(gitty_dir, "chroma")
    chroma_client = PersistentClient(path=persist_directory)
    try:
        collection = chroma_client.get_collection("issues")
    except Exception:
        collection = chroma_client.create_collection("issues")

    with closing(sqlite3.connect(db_path)) as conn:
        cursor = conn.execute("SELECT number, title, content FROM issues")
        rows = cursor.fetchall()

    sentence_transformer_ef = embedding_functions.DefaultEmbeddingFunction()

    for issue_number, title, content in rows:
        meta = {"title": title}
        embedding = sentence_transformer_ef([content])[0]
        collection.upsert(
            documents=[content],
            embeddings=[embedding],
            metadatas=[meta],
            ids=[str(issue_number)],
        )


# Updated function to fetch all issues and update the database.
def fetch_and_update_issues(owner: str, repo: str, db_path: Optional[str] = None) -> None:
    """
    Fetch all GitHub issues for the repo and update the local database.
    Only updates issues that have a more recent updatedAt timestamp.
    The database stores full issue content as produced by get_github_issue_content.
    If db_path is not provided, it is set to "<repo_root>/.gitty.db".
    """
    if db_path is None:
        gitty_dir = get_gitty_dir()
        db_path = os.path.join(gitty_dir, "issues.db")

    # Fetch issues using gh CLI (fetch summary without content)
    cmd = ["gh", "issue", "list", "--repo", f"{owner}/{repo}", "-L", "1000", "--json", "number,title,updatedAt"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        return
    try:
        issues = json.loads(result.stdout)
    except json.JSONDecodeError:
        return


    # Connect to or create the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS issues (
            number INTEGER PRIMARY KEY,
            title TEXT,
            updatedAt TEXT,
            content TEXT
        )
    """)

    # Pre-fetch existing issues to avoid N+1 queries
    cursor.execute("SELECT number, updatedAt FROM issues")
    existing_issues = {row[0]: row[1] for row in cursor.fetchall()}

    to_update = []
    to_insert = []

    for issue in tqdm(issues, desc="Fetching issues"):
        number = issue.get("number")
        title = issue.get("title")
        updatedAt = issue.get("updatedAt")

        if number in existing_issues:
            if updatedAt > existing_issues[number]:
                # Retrieve full issue content using the async method
                content = asyncio.run(get_github_issue_content(owner, repo, number))
                to_update.append((title, updatedAt, content, number))
        else:
            # Retrieve full issue content using the async method
            content = asyncio.run(get_github_issue_content(owner, repo, number))
            to_insert.append((number, title, updatedAt, content))

    if to_update:
        cursor.executemany(
            """
            UPDATE issues
            SET title = ?, updatedAt = ?, content = ?
            WHERE number = ?
        """,
            to_update,
        )
    if to_insert:
        cursor.executemany(
            """
            INSERT INTO issues (number, title, updatedAt, content)
            VALUES (?, ?, ?, ?)
        """,
            to_insert,
        )
    conn.commit()
    conn.close()
    print("Issue database update complete.")

    # Update Chroma DB with latest issues
    gitty_dir = get_gitty_dir()
    persist_directory = os.path.join(gitty_dir, "chroma")
    # Updated Chroma client construction (removed deprecated Settings usage)
    chroma_client = PersistentClient(path=persist_directory)
    try:
        collection = chroma_client.get_collection("issues")
    except Exception:
        collection = chroma_client.create_collection("issues")

    with closing(sqlite3.connect(db_path)) as conn:
        cursor = conn.execute("SELECT number, title, content FROM issues")
        rows = cursor.fetchall()

    # New embedding function using sentence_transformers
    sentence_transformer_ef = embedding_functions.DefaultEmbeddingFunction()

    for issue_number, title, content in rows:
        meta = {"title": title}  # metadata for each issue
        embedding = sentence_transformer_ef([content])[0]
        collection.upsert(
            documents=[content],
            embeddings=[embedding],
            metadatas=[meta],
            ids=[str(issue_number)],
        )
