import subprocess
import pathlib
import yaml

HERE = pathlib.Path().absolute()

def create_conda_environment(env_file, env_name):
    # Create Conda environment from environment file
    env_path = HERE / "devtools" / env_file
    assert env_path.exists(), f"No environment file {env_path} found."
    try:
        subprocess.run(f'mamba env remove -n {env_name}', check=False)
    except:
        pass  # fails if environment not present
    subprocess.run(f'mamba env create -f {env_path} -n {env_name} -q'.split(), check=True)
    subprocess.run(f'mamba install -n {env_name} pytest pytest-xdist nbval -c conda-forge -y -q'.split(), check=True)

def deactivate_conda_environment():
    # Deactivate Conda environment
    subprocess.run(['conda', 'deactivate'], shell=True, check=True)

def test_notebooks(notebooks, env_name):
    # Run tests on Jupyter notebooks
    success = True
    for notebook in notebooks:
        talktorial_path = HERE / "teachopencadd" / "talktorials" / notebook / "talktorial.ipynb"
        assert talktorial_path.exists(), f"Talktorial {notebook} not found."
        res = subprocess.run(f'conda run -n {env_name} pytest --nbval {talktorial_path}'.split())
        success = (res == 0) and success
    return success

def main():
    # Load configuration from YAML file
    with open('tests.yml', 'r') as file:
        config = yaml.safe_load(file)

    success = True
    for environment in config['environments']:
        env_name = environment['name']
        env_file = environment['file']
        notebooks = environment['notebooks']

        print(f"Setting up Conda environment '{env_name}'...")
        create_conda_environment(env_file, env_name)

        print(f"Running tests on Jupyter notebooks for environment '{env_name}'...")
        success = success and test_notebooks(notebooks, env_name)

    return success

if __name__ == "__main__":
    main()
