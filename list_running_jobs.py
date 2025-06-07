import sys
import json

# main
if __name__ == "__main__":
    data = sys.stdin.read()

    data = json.loads(data)
    print("Workflow Runs:")
    for workflow in data['workflow_runs']:
        print(
            f"\t --  {workflow['name']} |"
            f" {workflow['id']} |"
            f" {workflow['status']} |"
            f" {workflow['updated_at']} |"
            f" {workflow['artifacts_url']}"
        )