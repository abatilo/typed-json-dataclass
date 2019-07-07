workflow "Publish typed_json_dataclass" {
  on = "push"
  resolves = ["Publish"]
}

workflow "PR Builder" {
  on = "pull_request"
  resolves = ["Run flake8", "Run pytest"]
}

action "Install" {
  uses = "abatilo/actions-poetry@master"
  args = ["install"]
}

action "Run flake8" {
  needs = "Install"
  uses = "abatilo/actions-poetry@master"
  args = ["run", "python", "-m", "flake8", "--show-source", "--import-order-style", "pep8"]
}

action "Run pytest" {
  needs = "Install"
  uses = "abatilo/actions-poetry@master"
  args = ["run", "python", "-m", "pytest", "--cov-report", "xml:codecov.xml", "--cov=typed_json_dataclass", "--cov-report=html", "--junit-xml=coverage.xml", "--cov-branch", "--cov-fail-under=100", "tests/"]
}

action "Master branch" {
  needs = ["Run pytest", "Run flake8"]
  uses = "actions/bin/filter@master"
  args = "branch master"
}

action "Upload codecov" {
  needs = ["Master branch"]
  uses = "abatilo/actions-poetry@master"
  secrets = ["CODECOV_TOKEN"]
  args = ["run codecov -t $CODECOV_TOKEN"]
}

action "Publish" {
  needs = "Upload codecov"
  uses = "abatilo/actions-poetry@master"
  secrets = ["PYPI_USERNAME", "PYPI_PASSWORD"]
  args = ["publish", "--build", "--no-interaction", "-vv", "--username", "$PYPI_USERNAME", "--password", "$PYPI_PASSWORD"]
}
