"""Run the quickstart team's shell scripts as-is, with pytest as the harness.

The scripts live in ``tests/*.sh`` (one level up from this ``tests/ci/``
package). We shell out to them unmodified and turn a non-zero exit into a
pytest failure, surfacing the script's own output in the failure message.
"""

import pathlib
import subprocess

# tests/ -- parent of this tests/ci/ package, where the *.sh scripts live.
SCRIPTS_DIR = pathlib.Path(__file__).resolve().parents[1]

# Offline (no-cluster) quickstart scripts. Add new self-contained scripts here;
# each becomes its own parametrized test case. Cluster-dependent scripts need
# their own guarded list and are intentionally not included.
OFFLINE_SCRIPTS = ["test-oidc-templates.sh"]


def run_quickstart_script(script_name):
    """Run a quickstart shell script and assert it exits 0.

    Invoked as ``bash <abs-path>`` so the executable bit is irrelevant while the
    script can still derive SCRIPT_DIR/REPO_ROOT from ``$0``. On failure the
    captured stdout/stderr is included so the junit-xml report shows the
    script's own "N passed, M failed" summary.
    """
    script_path = SCRIPTS_DIR / script_name
    result = subprocess.run(
        ["bash", str(script_path)],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, (
        f"{script_name} failed (exit {result.returncode})\n"
        f"--- stdout ---\n{result.stdout}\n"
        f"--- stderr ---\n{result.stderr}"
    )
