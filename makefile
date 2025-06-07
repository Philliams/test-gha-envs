MAKEFLAGS += --no-print-directory

gha-runs:
	@gh api -H "Accept: application/vnd.github+json" -H "X-GitHub-Api-Version: 2022-11-28" repos/Philliams/test-gha-envs/actions/runs

gha-wf-run:
	gh api -H "Accept: application/vnd.github+json" -H "X-GitHub-Api-Version: 2022-11-28" repos/Philliams/test-gha-envs/actions/runs/15502481060/jobs

gha-wf-job:
	gh api -H "Accept: application/vnd.github+json" -H "X-GitHub-Api-Version: 2022-11-28" repos/Philliams/test-gha-envs/actions/jobs/43652075333/logs

test:
	gh api -H "Accept: application/vnd.github+json" -H "X-GitHub-Api-Version: 2022-11-28" https://api.github.com/repos/Philliams/test-gha-envs/actions/runs/15502481060/artifacts

test2:
	gh api -H "Accept: application/vnd.github+json" -H "X-GitHub-Api-Version: 2022-11-28" https://api.github.com/repos/Philliams/test-gha-envs/actions/artifacts/3279952695/zip

available-envs:
	make gha-runs | uv run list_running_jobs.py