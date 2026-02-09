import typer
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.panel import Panel
from rich.markdown import Markdown
from typing import Optional
import os
import sys

# Add src to path to ensure imports work if run directly
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from src.git_ops import GitOps
from src.llm import LLMClient
from src.analysis import Analyzer

app = typer.Typer()
console = Console()

@app.command()
def commit(repo_path: str = "."):
    """
    Smart commit with readiness checks and LLM-generated message.
    """
    try:
        git_ops = GitOps(repo_path)
    except ValueError as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        raise typer.Exit(code=1)

    # 1. Diff Analysis
    diff = git_ops.get_diff(staged=True)
    if not diff:
        console.print("[yellow]No staged changes found. Did you forget to 'git add'?[/yellow]")
        raise typer.Exit(code=0)
    
    changed_files = git_ops.get_changed_files(staged=True)

    # 2. Readiness Check
    analyzer = Analyzer()
    warnings = analyzer.check_readiness(diff, changed_files)
    
    console.print(Panel.fit("Checking Review Readiness...", title="git-scribe", border_style="blue"))
    
    for warning in warnings:
        if "⚠️" in warning:
             console.print(warning, style="bold yellow")
        else:
             console.print(warning, style="bold green")

    if any("⚠️" in w for w in warnings):
        if not Confirm.ask("Readiness checks flagged potential issues. Continue anyway?"):
            raise typer.Abort()

    # 3. LLM Generation
    console.print("[bold cyan]Generating commit message...[/bold cyan]")
    try:
        llm = LLMClient()
        commit_message = llm.generate_commit_message(diff)
    except Exception as e:
        console.print(f"[bold red]LLM Error:[/bold red] {e}")
        raise typer.Exit(code=1)

    console.print(Panel(commit_message, title="Proposed Commit Message", border_style="green"))

    # 4. Interaction
    choice = Prompt.ask("(a) accept/(e) edit/(c) cancel", choices=["accept", "edit", "cancel", "a", "e", "c"], default="accept")

    if choice in ["cancel", "c"]:
        console.print("Aborted.")
        raise typer.Abort()
    
    if choice in ["edit", "e"]:
        commit_message = typer.edit(commit_message)
        if not commit_message:
            console.print("Empty message, aborted.")
            raise typer.Abort()

    # 5. Execute
    git_ops.commit(commit_message)
    console.print("[bold green]Committed successfully![/bold green]")

@app.command()
def pr(repo_path: str = ".", main_branch: str = "main"):
    """
    Generate a Pull Request description based on branch history.
    """
    try:
        git_ops = GitOps(repo_path)
    except ValueError as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        raise typer.Exit(code=1)

    # 1. Get History & Diff
    commits = git_ops.get_branch_history(main_branch)
    if not commits:
        console.print(f"[yellow]No commits found different from {main_branch}.[/yellow]")
        # Often we might still want to proceed if there are staged changes, but usually PR is for pushed commits
        # Let's check for diff against main
    
    # We can get a diff against main to be sure
    # This might be heavy for large repos, but for now:
    try:
        diff = git_ops.repo.git.diff(main_branch)
    except Exception:
        diff = ""

    history_text = "\n".join([f"{c.hexsha[:7]} {c.summary}" for c in commits])
    
    # 2. LLM Generation
    console.print("[bold cyan]Generating PR description...[/bold cyan]")
    try:
        llm = LLMClient()
        pr_description = llm.generate_pr_description(diff, history_text)
    except Exception as e:
        console.print(f"[bold red]LLM Error:[/bold red] {e}")
        raise typer.Exit(code=1)
    
    console.print(Markdown(pr_description))
    
    # Optional: Copy to clipboard or save to file
    if Confirm.ask("Save to PULL_REQUEST_TEMPLATE.md?"):
        with open("PULL_REQUEST_TEMPLATE.md", "w") as f:
            f.write(pr_description)
        console.print("[bold green]Saved![/bold green]")


if __name__ == "__main__":
    app()
