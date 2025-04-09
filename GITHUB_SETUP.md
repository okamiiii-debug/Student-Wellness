# GitHub Setup Guide

Follow these steps to push this project to your GitHub repository:

## Step 1: Initialize Git (if not already done)

```bash
git init
```

## Step 2: Add Files to Git

```bash
git add .
```

This adds all the files in your project to Git, except those specified in the `.gitignore` file.

## Step 3: Commit the Changes

```bash
git commit -m "Initial commit of Student Wellness App"
```

## Step 4: Create a Repository on GitHub

1. Go to GitHub (https://github.com)
2. Log in to your account
3. Click on the "+" icon in the top right corner and select "New repository"
4. Name your repository (e.g., "student-wellness-app")
5. Add a description (optional)
6. Choose whether to make the repository public or private
7. Do NOT initialize the repository with a README, .gitignore, or license (we already have these)
8. Click "Create repository"

## Step 5: Link Your Local Repository to GitHub

After creating the repository, GitHub will show you commands to push an existing repository. Run these commands:

```bash
git remote add origin https://github.com/YOUR-USERNAME/YOUR-REPOSITORY-NAME.git
git branch -M main
git push -u origin main
```

Replace `YOUR-USERNAME` with your GitHub username and `YOUR-REPOSITORY-NAME` with the name you gave your repository.

## Step 6: Verify the Upload

Go to your GitHub repository URL to verify that all files have been uploaded correctly.

## Step 7: For Future Changes

After making changes to your code:

```bash
git add .
git commit -m "Description of changes made"
git push origin main
```

That's it! Your Student Wellness App is now on GitHub.

## Notes on Django Secret Key

For security reasons, it's best practice to keep your Django secret key out of version control. For a production deployment, consider using environment variables for the secret key.