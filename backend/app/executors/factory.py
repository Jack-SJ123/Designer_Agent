import os

from .autocad_executor import AutoCADExecutor
from .dry_run import DryRunExecutor
from .remote_runner import RemoteRunnerExecutor


def build_executor():
    mode = os.getenv("EDA_EXECUTOR_MODE", "dry_run").lower()
    if mode == "autocad":
        return AutoCADExecutor()
    if mode == "remote":
        return RemoteRunnerExecutor()
    return DryRunExecutor()
