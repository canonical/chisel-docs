import datetime
import os
import yaml
import textwrap

# Configuration for the Sphinx documentation builder.
# All configuration specific to your project should be done in this file.
#
# If you're new to Sphinx and don't want any advanced or custom features,
# just go through the items marked 'TODO'.
#
# A complete list of built-in Sphinx configuration values:
# https://www.sphinx-doc.org/en/master/usage/configuration.html
#
# Our starter pack uses the custom Canonical Sphinx extension
# to keep all documentation based on it consistent and on brand:
# https://github.com/canonical/canonical-sphinx


#######################
# Project information #
#######################

# Project name

project = "Chisel"
author = "Canonical Ltd."


# Sidebar documentation title; best kept reasonably short

version = f"{os.environ.get('READTHEDOCS_VERSION', 'local')}"

html_title = project + " documentation"


# Copyright string; shown at the bottom of the page
#
# Now, the starter pack uses CC-BY-SA as the license
# and the current year as the copyright year.

copyright = f"{datetime.date.today().year}"


# Documentation website URL

ogp_site_url = f"https://ubuntu.com/chisel/docs/{version}/"


# Preview name of the documentation website

ogp_site_name = project

# Preview image URL

ogp_image = "https://assets.ubuntu.com/v1/cc828679-docs_illustration.svg"


# Product favicon; shown in bookmarks, browser tabs, etc.

# TODO: To customise the favicon, uncomment and update as needed.

# html_favicon = '_static/favicon.png'


# Dictionary of values to pass into the Sphinx context for all pages:
# https://www.sphinx-doc.org/en/master/usage/configuration.html#confval-html_context

html_context = {
    # Product page URL; can be different from product docs URL
    "product_page": "github.com/canonical/chisel",
    # Your Discourse instance URL
    "discourse": "https://discourse.ubuntu.com/tags/c/rocks/117/chisel",
    # Your Mattermost channel URL
    #
    # TODO: Change to your Mattermost channel URL or leave empty.
    "mattermost": "",
    # Your Matrix channel URL
    "matrix": "https://matrix.to/#/#chisel:ubuntu.com",
    # Your documentation GitHub repository URL    #
    "github_url": "https://github.com/canonical/chisel-docs",
    # Docs branch in the repo; used in links for viewing the source files
    'repo_default_branch': 'main',
    # Docs location in the repo; used in links for viewing the source files
    "repo_folder": "/docs/",
    # TODO: To enable or disable the Previous / Next buttons at the bottom of pages
    # Valid options: none, prev, next, both
    # "sequential_nav": "both",
    # TODO: To enable listing contributors on individual pages, set to True
    "display_contributors": False,

    # Required for feedback button
    'github_issues': 'enabled',

    # Passes the top-level 'author' value to the theme
    "author": author,
    # Documentation license information
    "license": {
        "name": "CC-BY-SA-4.0",
        "url": "https://creativecommons.org/licenses/by-sa/4.0/",
    },
}

html_extra_path = []

# Allow opt-in build of the OpenAPI "Hello" example so docs stay clean by default.
if os.getenv("OPENAPI", ""):
    tags.add("openapi")
    html_extra_path.append("how-to/assets/openapi.yaml")

# TODO: To enable the edit button on pages, uncomment and change the link to a
# public repository on GitHub or Launchpad. Any of the following link domains
# are accepted:
# - https://github.com/example-org/example"
# - https://launchpad.net/example
# - https://git.launchpad.net/example
#
# html_theme_options = {
# 'source_edit_link': 'https://github.com/canonical/sphinx-docs-starter-pack',
# }

# Project slug; see https://meta.discourse.org/t/what-is-category-slug/87897
slug = 'chisel/docs' # Or '<ecosystem>/<product>/docs'

#######################
# Sitemap configuration: https://sphinx-sitemap.readthedocs.io/
#######################

# Use RTD canonical URL to ensure duplicate pages have a specific canonical URL

html_baseurl = f"https://ubuntu.com/chisel/docs/{version}/"

# URL scheme. Add language and version scheme elements.
# When configured with RTD variables, check for RTD environment so manual runs succeed:

if 'READTHEDOCS_VERSION' in os.environ:
    version = os.environ["READTHEDOCS_VERSION"]
    sitemap_url_scheme = '{link}'
else:
    sitemap_url_scheme = 'MANUAL/{link}'

# Include `lastmod` dates in the sitemap:

sitemap_show_lastmod = True
sitemap_filename = "doc-sitemap.xml"

# Exclude generated pages from the sitemap:

sitemap_excludes = [
    '404/',
    'genindex/',
    'search/',
]

#######################
# Template and asset locations
#######################

html_static_path = ["_static"]
templates_path = ["_static/_templates"]


#############
# Redirects #
#############

# Add redirects to the 'redirects.txt' file
# https://sphinxext-rediraffe.readthedocs.io/en/latest/

# Redirects for this project are managed in the Read the Docs project dashboard:
# https://docs.readthedocs.io/en/stable/guides/redirects.html
#rediraffe_redirects = "redirects.txt"

# Strips '/index.html' from destination URLs when building with 'dirhtml'
#rediraffe_dir_only = True

############################
# sphinx-llm configuration #
############################

# sphinx-llm config - https://github.com/NVIDIA/sphinx-llm
# Short description of your docs set:
llms_txt_description = (
    "This documentation provides guidance for using Chisel, a developer tool "
    "for extracting highly customized and specialized slices of Ubuntu "
    "packages to create minimal Ubuntu filesystems with a reduced attack surface "
    "and a small storage footprint. "
    "Ideal for building distroless-like Docker containers."
)

# The base URL for references built by sphinx-markdown-builder.
if os.environ.get("READTHEDOCS"):
    markdown_http_base = html_baseurl

###########################
# Link checker exceptions #
###########################

# A regex list of URLs that are ignored by 'make linkcheck'

linkcheck_ignore = [
    "http://127.0.0.1:8000",
    "https://www.gnu.org/*",
    r"https://matrix\.to/.*",
]

# A regex list of URLs where anchors are ignored by 'make linkcheck'

linkcheck_anchors_ignore_for_url = [r"https://github\.com/.*"]

# How long the link checker will wait for a response for each request
# give linkcheck multiple tries on failure
#linkcheck_timeout = 30
linkcheck_retries = 3

########################
# Configuration extras #
########################

# Custom MyST syntax extensions; see
# https://myst-parser.readthedocs.io/en/latest/syntax/optional.html
#
# NOTE: By default, the following MyST extensions are enabled:
#       substitution, deflist, linkify

myst_enable_extensions = set(
    ["substitution", "deflist", "linkify", "tasklist", "attrs_inline"]
)


# Custom Sphinx extensions; see
# https://www.sphinx-doc.org/en/master/usage/extensions/index.html

# NOTE: The canonical_sphinx extension is required for the starter pack.

extensions = [
    "canonical_sphinx",
    "notfound.extension",
    "sphinx_design",
    "sphinx_reredirects",
    "sphinx_tabs.tabs",
    "sphinxcontrib.jquery",
    "sphinxext.opengraph",
    "sphinx_config_options",
    "sphinx_contributor_listing",
    "sphinx_filtered_toctree",
    "sphinx_llm.txt",
    "sphinx_related_links",
    "sphinx_roles",
    "sphinx_terminal",
    "sphinx_ubuntu_images",
    "sphinx_youtube_links",
    "sphinxcontrib.cairosvgconverter",
    "sphinx_last_updated_by_git",
    "sphinx.ext.intersphinx",
    "sphinx_sitemap",
]

# Excludes files or directories from processing

exclude_patterns = [
    "doc-cheat-sheet*",
    ".venv*",
    "_dev",
]

# Adds custom CSS files, located under 'html_static_path'

html_css_files = [
    "css/custom.css",
    "https://assets.ubuntu.com/v1/d86746ef-cookie_banner.css",
]

# Adds custom JavaScript files, located under 'html_static_path'

html_js_files = [
    "https://assets.ubuntu.com/v1/287a5e8f-bundle.js",
    "js/overwrite_links.js",
]


# Feedback button at the top; enabled by default
#
# TODO: To disable the button, uncomment this.

# disable_feedback_button = True


# Your manpage URL
#
# TODO: To enable manpage links, uncomment and replace {codename} with required
#       release, preferably an LTS release (e.g. noble). Do *not* substitute
#       {section} or {page}; these will be replaced by sphinx at build time
#
# NOTE: If set, adding ':manpage:' to an .rst file
#       adds a link to the corresponding man section at the bottom of the page.

# manpages_url = 'https://manpages.ubuntu.com/manpages/{codename}/en/' + \
#     'man{section}/{page}.{section}.html'

# Workaround for https://github.com/canonical/canonical-sphinx/issues/34

if "discourse_prefix" not in html_context and "discourse" in html_context:
    html_context["discourse_prefix"] = html_context["discourse"] + "/t/"

# Workaround for substitutions.yaml

if os.path.exists('./reuse/substitutions.yaml'):
    with open('./reuse/substitutions.yaml', 'r') as fd:
        myst_substitutions = yaml.safe_load(fd.read())

# Add configuration for intersphinx mapping

intersphinx_mapping = {}

#Adding clickable checkboxes
#def setup(app):
    #app.add_js_file("tasklist.js")

#Removing bulletpoints created so checklists are clickable
def setup(app):
    app.add_css_file("tasklist.css")
    app.add_js_file("tasklist.js")  #checkbox-enabling JS
