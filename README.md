# 🖋️ git-scribe

**The Intelligence Layer for your Git workflow.**

`git-scribe` automates the narrative of your code. It turns your changes into meaningful, conventional commit messages and detailed Pull Request descriptions using the power of LLMs (OpenAI GPT-4o). It also acts as a "Team Lead" by performing pre-flight readiness checks before you commit.

---

## ✨ Features

- **🤖 AI-Generated Commits:** content-aware, semantic messages (Conventional Commits).
- **📝 One-Command PRs:** Generates full PR descriptions with summaries, type of change, and checklists.
- **🛡️ Review Readiness Checks:**
    - ⚠️ Warns if you modify logic without adding tests.
    - 🔒 Scans for potential secrets/keys in your code.
    - 🐍 Checks specific files for missing migrations (e.g., Django models).
- **✨ Beautiful TUI:** Built with `Rich` for a premium terminal experience.

---

## 🚀 Installation

### From PyPI (Coming Soon)
```bash
pip install git-scribe-cli
```

### From Source
```bash
git clone https://github.com/yourusername/git-scribe-cli.git
cd git-scribe
pip install .
```

---

## ⚙️ Configuration

`git-scribe` requires an OpenAI API Key to function.

```bash
export OPENAI_API_KEY="sk-..."
```

Add this to your `.bashrc` or `.zshrc` to make it permanent.

---

## 📖 Usage

### 1. Smart Commit (`scribe commit`)

Stage your changes and run:

```bash
scribe commit
```

**What happens:**
1.  **Readiness Check:** Scans your staged changes for issues (missing tests, secrets).
2.  **Generation:** An LLM analyzes your diff and proposes a commit message.
3.  **Review:** You see the formatted message.
    - Press **`a`** to Accept.
    - Press **`e`** to Edit.
    - Press **`c`** to Cancel.

### 2. PR Description (`scribe pr`)

Ready to push? Generate a PR description based on your branch history:

```bash
scribe pr --main-branch master
```

**What happens:**
1.  **Analysis:** Reads all commits on your current branch that are ahead of `master` (or `main`).
2.  **Generation:** Creates a Markdown-formatted PR description.
3.  **Save:** Options to save it to `PULL_REQUEST_TEMPLATE.md` or copy it.

---

## 🛠️ Development

To contribute or modify `git-scribe`:

1.  Clone the repo.
2.  Install dependencies: `pip install -e .`
3.  Run the tool: `python src/main.py commit`

---

## 📄 License

MIT
