import os
import sys
import subprocess
import pathlib
import yaml

HERE = pathlib.Path().absolute()
PYTEST_ARGS = "--nbval-lax --nbval-current-env --dist loadscope --numprocesses 4"


def create_conda_environment(env_file, env_name):
    # Create Conda environment from environment file
    env_path = HERE / "devtools" / env_file
    assert env_path.exists(), f"No environment file {env_path} found."
    # subprocess.run(f'mamba env remove -n {env_name}', check=False)
    subprocess.run(
        f"mamba env create -f {env_path} -n {env_name} -q".split(), check=True
    )
    subprocess.run(
        f"mamba install -n {env_name} pytest pytest-xdist nbval -c conda-forge -y -q".split(),
        check=True,
    )


def test_notebooks(notebooks, env_name):
    # Run tests on Jupyter notebooks
    talktorial_paths = " ".join(
        str(HERE / "teachopencadd" / "talktorials" / notebook / "talktorial.ipynb")
        for notebook in notebooks
    )
    result = subprocess.run(
        f"conda run -n {env_name} pytest {PYTEST_ARGS} {talktorial_paths}".split()
    )
    return 0 == result.returncode


def main():
    # Load configuration from YAML file
    with open(HERE / "devtools" / "test_configurations.yml", "r") as file:
        config = yaml.safe_load(file)

    success = True
    for environment in config["environments"]:
        env_name = environment["name"]
        env_file = environment["file"]
        notebooks = environment["notebooks"]

        print(f"Setting up Conda environment '{env_name}'...")
        create_conda_environment(env_file, env_name)

        print(f"Running tests on Jupyter notebooks for environment '{env_name}'...")
        res = test_notebooks(notebooks, env_name)
        success = success and res

    return success


if __name__ == "__main__":
    success = main()
    if success:
        sys.exit(os.EX_OK)
    else:
        sys.exit(os.EX_SOFTWARE)
