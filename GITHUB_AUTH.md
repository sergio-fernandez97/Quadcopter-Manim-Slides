# GitHub Authentication Setup (This Repository Only)

## Step 1: Create a Personal Access Token

1. Go to GitHub: https://github.com/settings/tokens
2. Click **"Generate new token"** → **"Generate new token (classic)"**
3. Give it a name like "Quadcopter-Deep-RL Project"
4. Select scopes: Check **`repo`** (full control of private repositories)
5. Click **"Generate token"**
6. **Copy the token immediately** (you won't see it again!)

## Step 2: Configure Git for This Repository

The repository is already configured to use credential storage locally. When you push, Git will prompt you for credentials:

- **Username**: `sergfer26` (your GitHub username)
- **Password**: Paste your Personal Access Token (NOT your GitHub password)

## Step 3: Push Your Code

```bash
git push -u origin main
```

When prompted:
- Username: `sergfer26`
- Password: `<paste your personal access token here>`

The credentials will be stored in `~/.git-credentials` and will only be used for this repository's remote URL.

## Verify Configuration

Check that credential helper is set locally (not globally):

```bash
# Local config (this repo only)
git config --local --list | grep credential

# Should show: credential.helper=store
```

## Security Note

- The token is stored in `~/.git-credentials` in plain text
- This is only for this repository's GitHub remote
- If you want to remove stored credentials: `git credential reject` then enter the URL when prompted
- Or manually edit `~/.git-credentials` to remove the line for github.com

## Alternative: Use SSH Instead

If you prefer SSH (more secure, no token needed):
```bash
git remote set-url origin git@github.com:sergfer26/Quadcopter-Manim-Slides.git
```











