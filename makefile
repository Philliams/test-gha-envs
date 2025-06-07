MAKEFLAGS += --no-print-directory

gha-runs:
	@gh api -H "Accept: application/vnd.github+json" -H "X-GitHub-Api-Version: 2022-11-28" repos/Philliams/test-gha-envs/actions/runs

check-envs:
	echo $$( python list_running_jobs.py $$(gh auth token))

status:
	make gha-runs | jq ".workflow_runs[] | (.id|tostring) + \" - \" +  .name + \" - \" + .status + \" - \" + .artifacts_url"

artifact:
	gh api -H "Accept: application/vnd.github+json" -H "X-GitHub-Api-Version: 2022-11-28" https://api.github.com/repos/Philliams/test-gha-envs/actions/runs/15502561838/artifacts

	# | (.id|tostring) + \" - \" +  .name + \" - \" + .status + \" - \" + .artifacts_url"

artifacts:
	gh api -H "Accept: application/vnd.github+json" -H "X-GitHub-Api-Version: 2022-11-28" \
	repos/Philliams/test-gha-envs/actions/runs \
	| jq '.workflow_runs[] | select(.name == "Simple-CI" and .status == "completed") | .artifacts_url' \
	| xargs -L1 | tr -d "\r" \
	| xargs -I {} gh api -H "Accept: application/vnd.github+json" -H "X-GitHub-Api-Version: 2022-11-28" {} \
	| jq ".artifacts[0].archive_download_url" \
	| xargs -L1 | tr -d "\r" \
	| xargs -I {} gh api -H "Accept: application/vnd.github+json" -H "X-GitHub-Api-Version: 2022-11-28" {}


gha-wf-run:
	gh api -H "Accept: application/vnd.github+json" -H "X-GitHub-Api-Version: 2022-11-28" repos/Philliams/test-gha-envs/actions/runs/15502481060/jobs

gha-wf-job:
	gh api -H "Accept: application/vnd.github+json" -H "X-GitHub-Api-Version: 2022-11-28" repos/Philliams/test-gha-envs/actions/jobs/43652075333/logs

test:
	gh api -H "Accept: application/vnd.github+json" -H "X-GitHub-Api-Version: 2022-11-28" https://api.github.com/repos/Philliams/test-gha-envs/actions/runs/15502561838/artifacts

test2:
	gh api -H "Accept: application/vnd.github+json" -H "X-GitHub-Api-Version: 2022-11-28" https://api.github.com/repos/Philliams/test-gha-envs/actions/artifacts/3279974406/zip

available-envs:
	make gha-runs | uv run list_running_jobs.py