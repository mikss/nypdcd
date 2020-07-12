# nypdcd
Parsing of NYPD complaints data

## Setup

1. **Install Xcode Command Line Tools:**
    1. open up a terminal, run `xcode-select --install`, and agree to the prompt.
1. **Clone this repository:**
    1. [set up an SSH key](https://help.github.com/en/articles/connecting-to-github-with-ssh);
    1. run
        ```
        mkdir -p ~/src/github/
        cd ~/src/github
        git clone git@github.com:mikss/nypdcd.git
        cd nypdcd
        ```
1. **Bootstrap your dev environment:**
  1. run `make`, which will install and set up
        1. [brew](https://brew.sh/) (package manager)
        1. [direnv](https://direnv.net) (env vars based on the current directory)
        1. [pre-commit](https://pre-commit.com/) (manage git hooks)
        1. a python [virtual environment](https://docs.python.org/3/tutorial/venv.html) with all dependencies;
    1. add the [direnv shell hook](https://direnv.net/docs/hook.html) to your shell config (e.g., `~/.zshrc`);
    1. refresh your shell with `exec $SHELL`.
1. **Fetch data:** run `make local-copy` to save a local copy of NYPD complaints data via [Socrata API](https://dev.socrata.com).

---

## TODO

* If move repo to public:
    - protect master branch;
    - ReviewNB integration;
    - GH actions for CI/CD (linting + testing).
