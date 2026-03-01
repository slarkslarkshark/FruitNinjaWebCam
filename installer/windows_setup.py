from __future__ import annotations

import argparse
import platform
import subprocess
import sys
from pathlib import Path

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover
    import tomli as tomllib  # type: ignore

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DIST_DIR = PROJECT_ROOT / "dist"
BUILD_DIR = PROJECT_ROOT / "build"
SPEC_FILE = PROJECT_ROOT / "FruitNinjaWebCam.spec"


def run(cmd: list[str]) -> None:
    print(">", " ".join(cmd))
    subprocess.run(cmd, check=True, cwd=PROJECT_ROOT)


def load_project_dependencies() -> list[str]:
    pyproject = PROJECT_ROOT / "pyproject.toml"
    data = tomllib.loads(pyproject.read_text(encoding="utf-8"))
    project = data.get("project", {})
    deps = project.get("dependencies", [])
    if not isinstance(deps, list):
        return []
    return [str(dep) for dep in deps]


def install_dependencies(include_builder: bool) -> None:
    run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])

    deps = load_project_dependencies()
    if deps:
        run([sys.executable, "-m", "pip", "install", *deps])

    if include_builder:
        run([sys.executable, "-m", "pip", "install", "pyinstaller>=6.0"])


def build_exe(onefile: bool) -> None:
    mode_flags = ["--onefile"] if onefile else ["--onedir"]
    run(
        [
            sys.executable,
            "-m",
            "PyInstaller",
            "--noconfirm",
            "--clean",
            "--windowed",
            *mode_flags,
            "--optimize",
            "2",
            "--name",
            "FruitNinjaWebCam",
            "--collect-all",
            "mediapipe",
            "--exclude-module",
            "pygame.tests",
            "--exclude-module",
            "mediapipe.tasks.python.test",
            "--exclude-module",
            "mediapipe.tasks.python.benchmark",
            "--exclude-module",
            "matplotlib.tests",
            "--exclude-module",
            "numpy.tests",
            "--exclude-module",
            "jax",
            "--exclude-module",
            "jaxlib",
            "--exclude-module",
            "scipy",
            "--hidden-import",
            "shapely",
            "--hidden-import",
            "shapely.geometry",
            "main.py",
        ]
    )


def print_result() -> None:
    print("\nBuild completed.")
    print(f"Output directory: {DIST_DIR}")
    print("Default output is a single file: dist/FruitNinjaWebCam.exe")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Install deps and build Windows .exe")
    parser.add_argument(
        "--install-only",
        action="store_true",
        help="Install dependencies only (no build).",
    )
    parser.add_argument(
        "--build",
        action="store_true",
        help="Build executable after installation.",
    )
    parser.add_argument(
        "--onefile",
        action="store_true",
        help="Build a single .exe file (default mode).",
    )
    parser.add_argument(
        "--onedir",
        action="store_true",
        help="Build as folder (faster startup, larger delivery size).",
    )
    parser.add_argument(
        "--skip-os-check",
        action="store_true",
        help="Allow running outside Windows (useful for CI scripting).",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    if not args.skip_os_check and platform.system() != "Windows":
        print("This setup module is intended to run on Windows.")
        print("Use --skip-os-check only if you know what you are doing.")
        return 1

    should_build = args.build or not args.install_only

    install_dependencies(include_builder=should_build)

    if should_build:
        # Clean previous build artifacts to reduce confusion between runs.
        if BUILD_DIR.exists():
            print(f"Cleaning {BUILD_DIR}")
        if SPEC_FILE.exists():
            print(
                f"Note: existing spec file {SPEC_FILE.name} may be overwritten by PyInstaller."
            )
        use_onefile = args.onefile or not args.onedir
        build_exe(onefile=use_onefile)
        print_result()
    else:
        print("Dependencies installed. Build was skipped.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
