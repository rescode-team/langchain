import subprocess
from pathlib import Path

from langchain.utilities.bash import BashProcess

def test_pwd_command() -> None:
    """Test correct functionality."""
    session = BashProcess()
    commands = ["pwd"]
    output = session.run(commands)
    print(output)

    assert output["outputs"] == [subprocess.check_output("pwd", shell=True).decode()]

def test_incorrect_command() -> None:
    """Test handling of incorrect command."""
    session = BashProcess()
    output = session.run(["invalid_command"])
    assert output["success"] is False

def test_create_directory_and_files(tmp_path: Path) -> None:
    """Test creation of a directory and files in a temporary directory."""
    session = BashProcess(strip_newlines=True)

    # create a subdirectory in the temporary directory
    temp_dir = tmp_path / "test_dir"
    temp_dir.mkdir()

    # run the commands in the temporary directory
    commands = [
        f"touch {temp_dir}/file1.txt",
        f"touch {temp_dir}/file2.txt",
        f"echo 'hello world' > {temp_dir}/file2.txt",
        f"cat {temp_dir}/file2.txt"
    ]

    output = session.run(commands)
    assert output["success"] is True
    assert output["outputs"][-1] == "hello world"

    # check that the files were created in the temporary directory
    output = session.run([f"ls {temp_dir}"])
    assert output["success"] is True
    assert output["outputs"] == ["file1.txt\nfile2.txt"]
