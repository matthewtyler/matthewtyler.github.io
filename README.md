# Matthew Tyler’s website

A static Jekyll site with a compact profile introduction, full-width research
lists, desktop sticky navigation, and a graduate-study reading page. The design uses
locally hosted WOFF2 Literata in the same fixed styles requested by Econvitals,
with 16px body text, compact bold headings, narrower reading columns, blue accents, and
fine section dividers on a soft charcoal background with warm off-white text.
Printed pages use a white background. It supports mobile
layouts, keyboard navigation, reduced motion, and printing. Content and navigation work without
JavaScript; a small script optionally highlights the active homepage section.

Edit the biography in `index.md`, profile details in `_config.yml`, and graduate
information in `graduate-study.md`. Presentation lives in
`_layouts/homepage.html`, `_includes/research.html`, and
`_sass/minimal-light.scss`. Publication data in `_data/publications.json` is
generated from the CV; do not edit it by hand. Existing publication anchors,
`/graduate-study.html`, and the CV download path are preserved.

Run `bundle exec jekyll serve` to preview at <http://localhost:4000>.

The original theme documentation is retained below for reference.

## Research topics

Edit `_data/research_topics.json` to change the filter labels and each paper's
topics. These are editorial assignments, separate from the CV-generated citation
data. The `papers` keys must match titles in `_data/publications.json` exactly;
update the corresponding key if a title changes. A paper can have several topics.
New papers without topic metadata still appear under **All research**.

Use **Methods** for work whose central contribution concerns estimation,
identification, research design, or measurement validity (including survey error).
Use **American Politics** for substantive work on US elections, political behavior,
public opinion, or institutions. Assign both when both contributions are central;
using statistical methods alone does not warrant Methods, and a US illustration
alone does not warrant American Politics.

The assignments were reviewed against available abstracts and paper descriptions.
The campaign paper remains classified from its title because no public abstract
was located; the Designing for Power classification relies on its title and
indexed SSRN keywords because the full abstract was inaccessible.

One filter is active at a time. Counts update across all publication categories;
empty categories remain visible. The full list and labels work without JavaScript,
and printing includes all papers even while a filter is selected.

Run `node script/tests/test_research_filter.js` to check filter behavior and
`python3 -m unittest discover -s script/tests` to check CV parsing and topic metadata.
The filter implementation lives in `assets/js/research-filter.js`.

## Updating the CV and publications

`CV/CV.tex` is the source of truth for the website's publication lists,
including working papers and invited articles. The website displays peer reviewed
articles, working papers, and then invited articles under “Other Publications.” After editing the CV, run:

```sh
script/build-cv
```

This rebuilds `CV/CV-Matthew-Tyler.pdf` and automatically updates the publication
data in `_data/publications.json`. Commit the LaTeX source, PDF, and JSON together. To sync just the website
without a LaTeX installation, run `python3 script/sync-publications`.

Do not edit the generated `_data/publications.json` file. CI checks it against the CV on every push and pull request and fails
if it is out of date. Keep publications in the CV's `publicationlist` and
`manuscriptlist` environments; unsupported LaTeX produces an error rather than
silently dropping content. Editing only the PDF does not update the source or
website; make CV changes in `CV/CV.tex`.

[![LICENSE](https://img.shields.io/github/license/yaoyao-liu/minimal-light?style=flat-square&logo=creative-commons&color=EF9421)](https://github.com/yaoyao-liu/minimal-light/blob/main/LICENSE)
[![gem](https://img.shields.io/gem/v/minimal-light?style=flat-square&logo=rubygems&color=E9573F)](https://rubygems.org/gems/minimal-light)
[![Jekyll](https://img.shields.io/badge/jekyll-%3E%3D%203.5-orange.svg?style=flat-square&logo=jekyll)](https://jekyllrb.com/)
[![Build Status](https://img.shields.io/travis/com/yaoyao-liu/minimal-light?style=flat-square&logo=travis-ci&color=3EAAAF)](https://travis-ci.com/yaoyao-liu/minimal-light)

\[[Demo the theme](https://minimal-light.yyliu.net/)\]  \[[简体中文](https://github.com/yaoyao-liu/minimal-light/blob/master/README_zh_Hans.md) | [繁體中文](https://github.com/yaoyao-liu/minimal-light/blob/master/README_zh_Hant.md) | [Deutsche](https://github.com/yaoyao-liu/minimal-light/blob/master/README_de.md)\]
 
*This is the source code of my homepage. I build this website based on [minimal](https://github.com/orderedlist/minimal).*
<br>
*Feel free to use and share the source code anywhere you like.*

## Features

- Simple and elegant personal homepage theme
- Jekyll theme, deploy automatically by GitHub pages
- Basic Search Engine Optimization
- Mobile friendly
- Support Markdown 
- Support dark mode

## Usage

### Using on GitHub 

To use this theme, add the following to your repository's `_config.yml`:

```yaml
remote_theme: yaoyao-liu/minimal-light
```

Please note that adding the above line will directly apply all the default settings in this repository to yours.

If you hope to edit any files (e.g., `index.md`), you still need to copy them to your repository.

You may also fork this repository (or [use this repository as a template](https://docs.github.com/en/github/creating-cloning-and-archiving-repositories/creating-a-repository-from-a-template)) and change the name to `your-username.github.io`.

Then you need to enable the GitHub pages for that repository following the steps [here](https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site#creating-your-site).

#### Using a custom domain on GitHub

Add a `CNAME` DNS record to your domain as follows:
```
Host: whatever you want. e.g., "www" 
Target / Canonical name: your-username.github.io.
TTL: 10 min
```
You may also add an `A` DNS record instead of the `CNAME` record as follows:
```
Host: whatever you want. e.g., "www" or "@"
IP: 185.199.108.153
    185.199.109.153
    185.199.110.153
    185.199.111.153
TTL: 10 min
```

Then, change the contents of the [CNAME](./CNAME) file in this repository to your domain.

### Using Locally with Jekyll

*You need to install [Ruby](https://www.ruby-lang.org/en/) and [Jekyll](https://jekyllrb.com/) fisrt.*

Clone this repository:

```bash
git clone https://github.com/yaoyao-liu/minimal-light.git
cd minimal-light
```
Install and run:

```bash
bundle install
bundle exec jekyll server
```
View the live page using `localhost`:
<http://localhost:4000>. You can get the html files in `_site` folder.

## Customizing

### Configuration variables

The Minimal Light theme will respect the following variables, if set in your site's `_config.yml`:

  ```yaml
title: Your Name
affiliation: Your Affiliation
email: yourname (at) example.edu
google_scholar: https://scholar.google.com/
github_link: https://github.com/yaoyao-liu/minimal-light
linkedin: https://www.linkedin.com/
avatar: ./assets/img/avatar.png
google_analytics: UA-111540567-4
favicon: ./assets/img/favicon.png
favicon_dark: ./assets/img/favicon-dark.png
description: The Minimal Light is a simple and elegant jekyll theme for academic personal homepage.
canonical: https://minimal-light.yyliu.net/
remote_theme: yaoyao-liu/minimal-light
  ```
### Editing `index.md`

Create `index.md` and add your personal information (e.g. publications, research).

### Stylesheet

If you'd like to add your own custom styles:

1. Create a file called `/assets/css/style.scss` in your site
2. Add the following content to the top of the file, exactly as shown:

    ```scss
    ---
    ---

    @import "{{ site.theme }}";
    ```
3. Add any custom CSS (or Sass, including imports) you'd like immediately after the `@import` line

### Layouts

If you'd like to change the theme's HTML layout:

1. [Copy the original template](https://github.com/yaoyao-liu/minimal-light/blob/master/_layouts/homepage.html) from the theme's repository<br />(*Pro-tip: click "raw" to make copying easier*)
2. Create a file called `/_layouts/homepage.html` in your site
3. Paste the default layout content copied in the first step
4. Customize the layout as you'd like

## License

This work is licensed under a [Creative Commons Zero v1.0 Universal](https://github.com/yaoyao-liu/minimal-light/blob/master/LICENSE) License.

## Acknowledgements

Our project uses the source code from the following repositories:

* [pages-themes/minimal](https://github.com/pages-themes/minimal)

* [orderedlist/minimal](https://github.com/orderedlist/minimal)
