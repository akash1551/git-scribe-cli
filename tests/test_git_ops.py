import pytest
from unittest.mock import MagicMock, patch
from git_scribe.git_ops import GitOps

@patch('git.Repo')
def test_git_ops_init(mock_repo):
    git_ops = GitOps(".")
    mock_repo.assert_called_once()

@patch('git.Repo')
def test_get_diff(mock_repo):
    mock_git = MagicMock()
    mock_git.diff.return_value = "fake diff"
    mock_repo.return_value.git = mock_git
    
    git_ops = GitOps(".")
    diff = git_ops.get_diff(staged=True)
    
    assert diff == "fake diff"
    mock_git.diff.assert_called_with("--cached")
