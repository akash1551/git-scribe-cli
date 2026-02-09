import git
from typing import List, Optional
import os

class GitOps:
    def __init__(self, repo_path: str = "."):
        try:
            self.repo = git.Repo(repo_path, search_parent_directories=True)
        except git.InvalidGitRepositoryError:
            raise ValueError("Not a valid git repository")

    def get_diff(self, staged: bool = True) -> str:
        """Get the diff of changes."""
        if staged:
            return self.repo.git.diff("--cached")
        return self.repo.git.diff()

    def get_changed_files(self, staged: bool = True) -> List[str]:
        """Get list of changed files."""
        if staged:
            return [item.a_path for item in self.repo.index.diff("HEAD")]
        # For unstaged, it's a bit more complex with untracked files, 
        # but for now let's focus on modified tracked files for simplicity or rely on git diff --name-only
        return self.repo.git.diff("--name-only").splitlines()

    def commit(self, message: str) -> None:
        """Commit staged changes."""
        self.repo.index.commit(message)

    def get_branch_history(self, main_branch: str = 'main') -> List[git.Commit]:
        """Get commits unique to the current branch compared to main."""
        # This is a simplification. Ideally, we want commits in HEAD not in main.
        try:
            commits = list(self.repo.iter_commits(f'{main_branch}..HEAD'))
            return commits
        except git.exc.GitCommandError:
            # Fallback if main branch doesn't exist or other error
            return []

    def get_current_branch(self) -> str:
        return self.repo.active_branch.name
