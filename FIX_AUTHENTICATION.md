# 🔐 Fix GitHub Authentication (403 Error)

## Problem
You're getting a 403 "Permission denied" error when trying to push. This means GitHub is rejecting your authentication.

## Solution: Use Personal Access Token

GitHub no longer accepts passwords for HTTPS authentication. You need to use a **Personal Access Token** instead.

### Step 1: Create Personal Access Token

1. Go to GitHub: https://github.com/settings/tokens
2. Click **"Generate new token"** → **"Generate new token (classic)"**
3. Give it a name: `EduLingua Pro Push`
4. Select expiration: Choose your preference (90 days, 1 year, or no expiration)
5. **Select scopes**: Check `repo` (this gives full repository access)
6. Click **"Generate token"**
7. **IMPORTANT**: Copy the token immediately! You won't be able to see it again.

### Step 2: Push Using Token

When you run `git push`, it will ask for:
- **Username**: `R-Nishanth88`
- **Password**: Paste your Personal Access Token (NOT your GitHub password)

### Step 3: Alternative - Use SSH (Recommended)

SSH keys are more secure and don't require entering credentials each time.

#### Generate SSH Key (if you don't have one):
```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
# Press Enter to accept default location
# Press Enter twice for no passphrase (or set one if you want)
```

#### Add SSH Key to GitHub:
```bash
# Copy your public key
cat ~/.ssh/id_ed25519.pub
```

1. Copy the entire output
2. Go to: https://github.com/settings/keys
3. Click **"New SSH key"**
4. Paste the key and save

#### Update Remote to Use SSH:
```bash
git remote set-url origin git@github.com:R-Nishanth88/Edulingua.git
git push -u origin main
```

---

## Quick Fix Commands

### Option 1: HTTPS with Token
```bash
# Remote is already set, just push
git push -u origin main
# When prompted:
# Username: R-Nishanth88
# Password: [paste your Personal Access Token]
```

### Option 2: Switch to SSH
```bash
# Change remote to SSH
git remote set-url origin git@github.com:R-Nishanth88/Edulingua.git

# Push
git push -u origin main
```

---

## Verify Authentication

After pushing successfully, you should see:
```
Enumerating objects: 130, done.
Counting objects: 100% (130/130), done.
...
To https://github.com/R-Nishanth88/Edulingua.git
 * [new branch]      main -> main
Branch 'main' set up to track remote branch 'main' from 'origin'.
```

