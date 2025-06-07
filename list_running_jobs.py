import sys
import json
import requests
from zipfile import ZipFile
import io

def make_request(url, token, params={}, return_raw=False):
    response = requests.get(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "Authorization": f"Bearer {token}"
        },
        params=params
    )

    if return_raw:
        return response.content
    else:
        return json.loads(response.text)

def parse_zip_data(zip_bytestring):
    with ZipFile(io.BytesIO(zip_bytestring)) as zip_f:
        with zip_f.open('env.txt') as f:
            return f.read().decode("utf-8").replace("\n", "")

# main
if __name__ == "__main__":
    token = sys.stdin.read().replace("\n", "")

    envs = make_request(
  	    url="https://api.github.com/repos/Philliams/test-gha-envs/environments",
        token=token
    )

    env_names = [
        env['name']
        for env in envs['environments']
    ]

    data = make_request(
        url="https://api.github.com/repos/Philliams/test-gha-envs/actions/runs",
        token=token,
        params={
            "per_page": 2,
            "page": 1
        }
    )

    for workflow in data['workflow_runs']:

        print(
            f"\t --  {workflow['name']} |"
            f" {workflow['id']} |"
            f" {workflow['status']} |"
            f" {workflow['updated_at']} |"
            f" {workflow['artifacts_url']}"
        )

        name_check = workflow['name'] == "Simple-CI"
        status_check = workflow['status'] == "completed"

        if name_check and status_check:
            artifacts_url = workflow['artifacts_url']

            artifact_manifest = make_request(
                artifacts_url,
                token=token
            )

            assert artifact_manifest['total_count'] == 1
            zip_url = artifact_manifest['artifacts'][0]['archive_download_url']
            artifact_data = make_request(
                zip_url,
                token,
                return_raw=True
            )

            env_name = parse_zip_data(artifact_data)
            print(f"env name : {env_name}")