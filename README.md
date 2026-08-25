# Uchiha Mabben — Security Research

The source for Mohamed Aniss Benstaali's cybersecurity research and privacy-engineering blog, built with the [Jekyll Chirpy theme](https://github.com/cotes2020/jekyll-theme-chirpy) and deployed through GitHub Pages.

## Local development

```shell
bundle install
bundle exec jekyll serve
```

The project is configured as a GitHub Pages project site. Local posts live in `_posts`, navigation pages in `_tabs`, and media in `assets/img`.

## Publishing

Pushes to `main` trigger the included GitHub Actions workflow. The workflow builds the production site, validates the generated HTML, and deploys the resulting artifact to GitHub Pages.

## Content policy

Published material is intended for authorized security testing, reproducible research, and defensive education. Do not use it to test systems without permission.
