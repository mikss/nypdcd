# nypdcd
Parsing of NYPD complaints data

## Setup

1. **Install Xcode Command Line Tools:** open up a terminal, run `xcode-select --install`, and agree to the prompt.
1. **Clone this repository:** [set up an SSH key](https://help.github.com/en/articles/connecting-to-github-with-ssh) and then run
    ```
    mkdir -p ~/src/github/
    cd ~/src/github
    git clone git@github.com:mikss/nypdcd.git
    cd nypdcd
    ```
1. **Bootstrap your dev environment:** run `make` to install [brew](https://brew.sh/) (package manager) + [direnv](https://direnv.net) (env
vars based on the current directory) + [pre-commit](https://pre-commit.com/) (manage git hooks), and set up a python [virtual
environment](https://docs.python.org/3/tutorial/venv.html) with all dependencies. Then add the [direnv shell hook](https://direnv.net/docs/hook.html) to your shell config (e.g., `~/.zshrc`) and refresh your shell with `exec $SHELL`.
1. **Fetch data:** run `make local-copy` to save a local copy of NYPD complaints data via [Socrata API](https://dev.socrata.com).

## TODO

* if move repo to public:
    - protect master branch
    - ReviewNB integration
    - GH actions for CI/CD (linting + testing)
