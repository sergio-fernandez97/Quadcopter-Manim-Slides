# Git Configuration for This Project

## Configure Local Git Credentials

To set your GitHub username and email **only for this project**, run:

```bash
cd "/Users/sergio.fernandez/Documents/personal/tesis /Quadcopter-Deep-RL"

# Set your GitHub username (replace with your actual username)
git config user.name "YourGitHubUsername"

# Set your GitHub email (replace with your actual email)
git config user.email "your.email@example.com"
```

## Verify Configuration

Check that the local config is set correctly:

```bash
git config --local --list
```

You should see:
- `user.name=YourGitHubUsername`
- `user.email=your.email@example.com`

## Check Global vs Local

To see the difference:

```bash
# Global config (affects all repositories)
git config --global --list

# Local config (only this repository)
git config --local --list
```

## Optional: Set Up Remote Repository

If you want to connect this to a GitHub repository:

```bash
# Add remote (replace with your repository URL)
git remote add origin https://github.com/YourUsername/your-repo-name.git

# Verify remote
git remote -v
```

## Notes

- Local config (`--local`) overrides global config (`--global`) for this repository
- These settings are stored in `.git/config` in this repository
- Other repositories will use your global settings (if any)

