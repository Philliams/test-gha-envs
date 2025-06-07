MAKEFLAGS += --no-print-directory

gha-runs:
	@gh api -H "Accept: application/vnd.github+json" -H "X-GitHub-Api-Version: 2022-11-28" repos/Philliams/test-gha-envs/actions/runs

available-envs:
	make gha-runs | uv run list_running_jobs.py