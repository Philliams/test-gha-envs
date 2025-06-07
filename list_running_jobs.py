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

def get_active_runs(token):

    all_captured = False
    page = 1

    active_workflows = []    

    while not all_captured:

        workflows = make_request(
            url="https://api.github.com/repos/Philliams/test-gha-envs/actions/runs",
            token=token,
            params={
                "per_page": 2,
                "page": page
            }
        )

        if len(workflows['workflow_runs']) == 0:
            break

        for wf in workflows['workflow_runs']:
            name_check = wf['name'] == "Simple-CI"
            status_check = wf['status'] == "completed"

            if name_check and status_check:
                active_workflows.append(wf)
            elif not status_check:
                break
        
        page += 1
    
    return active_workflows

def parse_zip_data(zip_bytestring):
    with ZipFile(io.BytesIO(zip_bytestring)) as zip_f:
        with zip_f.open('env.txt') as f:
            return f.read().decode("utf-8").replace("\n", "")

def retrieve_artifact(artifacts_url, token):
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

    return env_name

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

    active_wfs = get_active_runs(token)
    counts = {e: 0 for e in env_names}


    for workflow in active_wfs:
        name_check = workflow['name'] == "Simple-CI"
        status_check = workflow['status'] == "completed"

        if name_check and status_check:
            try:
                env_name = retrieve_artifact(workflow['artifacts_url'], token)
                counts[env_name] += 1
            except Exception as e:
                pass

    next_env_to_use = min(counts, key=counts.get)
    print(next_env_to_use)