#!/usr/bin/env python3

import os
import sys
import json
import argparse
import subprocess
import urllib3
import requests

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_projects(gitlab_url, headers, page=1):
    print(f"Fetching projects from page {page}...")
    try:
        response = requests.get(f"https://{gitlab_url}/api/v4/projects", headers=headers, params={"membership": "true", "page": page, "per_page": 100}, verify=False)
        response.raise_for_status()

        try:
            projects_json = response.json()
        except json.JSONDecodeError as json_err:
            print(f"Failed to parse JSON response: {json_err}", file=sys.stderr)
            return None, response.headers

        print(f"Fetched projects successfully from page {page}")
        return projects_json, response.headers

    except requests.exceptions.RequestException as e:
        print(f"Failed to get projects: {e}", file=sys.stderr)
        return None, None

def clone_repository(gitlab_url, project_path_with_namespace, destination_path, headers, token):
    clone_url = f"https://oauth2:{token}@{gitlab_url}/{project_path_with_namespace}.git"
    print(f"Cloning repository {project_path_with_namespace} to {destination_path}...")
    try:
        os.makedirs(destination_path, exist_ok=True)
        subprocess.call(["git", "init", "--bare", "--quiet"], cwd=destination_path)
        subprocess.run(["git", "fetch", "--force", "--prune", "--tags", clone_url, "refs/heads/*:refs/heads/*",], cwd=destination_path, check=True)
        print(f"Cloned {clone_url} to {destination_path}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to clone {clone_url}: {e}", file=sys.stderr)

def main():
    parser = argparse.ArgumentParser(description="Backup GitLab repositories")
    parser.add_argument("config", metavar="CONFIG", help="a configuration file")
    args = parser.parse_args()

    print(f"Reading configuration from {args.config}...")
    with open(args.config, "r") as f:
        try:
            config = json.load(f)
        except json.JSONDecodeError as json_err:
            print(f"Failed to parse JSON configuration file: {json_err}", file=sys.stderr)
            return

    token = config["token"]
    gitlab_url = config["gitlab_url"]
    path = os.path.expanduser(config["directory"])

    print(f"Using GitLab URL: {gitlab_url}")
    print(f"Using backup directory: {path}")

    try:
        os.makedirs(path, exist_ok=True)
        print(f"Created directory {path}", file=sys.stderr)
    except FileExistsError:
        pass

    # headers = {"Authorization": f"Bearer {token}"}
    headers = {"Private-Token": token}
    page = 1

    while True:
        try:
            print(f"Fetching projects, page {page}...")
            projects, headers = get_projects(gitlab_url, headers, page)
        except requests.exceptions.RequestException as e:
            print(f"Failed to get projects: {e}", file=sys.stderr)
            break

        if projects is None:
            break

        for project in projects:
            namespace = project['namespace']['full_path']
            repo_name = project['path_with_namespace']
            project_id = project['id']

            # Construct the destination path
            namespace_path = os.path.join(path, namespace)
            os.makedirs(namespace_path, exist_ok=True)
            destination_path = os.path.join(namespace_path, repo_name.split('/')[-1])  # Use last part of path_with_namespace

            print(f"Cloning {project['name']} into {destination_path}")
            clone_repository(gitlab_url, project['path_with_namespace'], destination_path, headers, token)

        # Check if there are more pages
        next_page = headers.get('X-Next-Page')
        if not next_page:
            break
        page = int(next_page)

    print("Backup process completed.")

if __name__ == "__main__":
    main()
