# Git-good course itinerary:

## Introduction
0. Open terminal [x]
1. Setup SSH key [x]
    - https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account?platform=mac
    - Use guide for your OS

## Your GitHub repository
2. Have a look at our repository [x]
3. Make your own repository [x]
    - git init [x]
    - git clone [x]

## Collaborative Effort
4. Look at our repository again [x]
5. Clone our repository [x]
    - git clone <ssh>
6. Make your branch
    - git checkout -b "branch name"
    - git switch "branch name"
7. Make your changes [x]
    - Read the README [x]
    - Perform the task 

commands:
----------------
- git add .
- git commit -m "your message"
- git push

check state of your repo:
- git status
- git log (view commit history)

need remote changes?:
- git fetch
- git pull

branching:
- git branch (have a look at your branch)
- git checkout -b feat/descriptive_branch
- git push --set-upstream origin feat/newBranch
- git checkout "commit_id"
- git switch - (go back to the previous branch)


