[![Documentation Status](https://readthedocs.com/projects/canonical-chisel/badge/?version=latest)](https://canonical-chisel.readthedocs-hosted.com/en/latest/?badge=latest)

# Chisel documentation

Sources for building the [Chisel documentation].


## Chisel repositories

- [chisel] - main repository of the project
- [chisel-docs] - documentation repository
- [chisel-releases] - collection of package slice definitions


## Contribution guides

Prior to contributing, you must -

- read and get acquainted with the [Ubuntu Code of Conduct] and
- sign the [Canonical contributor license agreement].


### Style guides

The documentation follows the [Diataxis] principles.

The commits follow the [Conventional Commits v1.0.0] guidelines.


### Configure your environment

Chisel documentation is built on top of [Sphinx starter pack] and hosted on
[Read the Docs].

To work on the project, you will need to have Python, `python3.12-venv`, and `make` packages.

```bash
sudo apt install make python3 python3.12-venv
```


### Build documentation locally

The Makefile in the [docs/](docs/) directory contains many targets. To see all
possible `make` commands, run `make help`.

To watch, build and serve the document, run `make run`. To learn more, check
out the [Sphinx starter pack website].


### Submit a pull request

After submitting a pull request, a few Github workflows run automatically to
test the changes. If one of those fails, click on the failing workflow to see
the logs to troubleshoot.

Note: more tests will be added in the future.
<!-- TODO: update the tests description once there are more -->

After submitting a pull request, your changes will be reviewed by a project
maintainer.


### Custom page meta descriptions

The meta description provides a summary of the page. Search engines often reuse this for the search result’s snippet.

All **new** pages must include a meta description. To set custom HTML meta descriptions in MyST-MD, use front matter at the top of the document as shown below:

```
---
myst:
  html_meta:
    description: Your description of the page.
---
```

Please observe the following guidelines:

- Use a maximum of 160 characters.
- Summarize the content of the page, where possible.
- Keep the language simple, avoid unnecessary adverbs or adjectives.
- Use an informative tone, frame sentences in terms of actions and facts.
- Use the tool name and page-specific terminology that users are likely to use when searching for information. 
- Place key terms near the start.
- Don’t include key terms that aren’t on the page.
  

### Get help

If you are a new contributor to documentation in general and would like some
guidance, you can check out the [Open Documentation Academy repository] or ask
a question on [Open Documentation Academy discourse].


## Report issues

To report issues or feature requests regarding the documentation, please fill
out an issue in the [chisel-docs] repository.

For issues regarding Chisel itself, please report them in the [chisel]
repository.


## Contact

To contact the maintainers for any purposes, please use the [Chisel room in Matrix].


<!-- LINKS -->

[Chisel documentation]: https://documentation.ubuntu.com/chisel/en/latest
[Canonical contributor license agreement]: https://ubuntu.com/legal/contributors
[Chisel room in Matrix]: https://matrix.to/#/#chisel:ubuntu.com
[Conventional Commits v1.0.0]: https://www.conventionalcommits.org/en/v1.0.0/
[Diataxis]: https://diataxis.fr/
[Read the Docs]: https://about.readthedocs.com/
[Sphinx starter pack website]: https://canonical-starter-pack.readthedocs-hosted.com/dev/how-to/build/
[Sphinx starter pack]: https://github.com/canonical/sphinx-docs-starter-pack
[Ubuntu Code of Conduct]: https://ubuntu.com/community/ethos/code-of-conduct
[Open Documentation Academy repository]: https://github.com/canonical/open-documentation-academy/
[Open Documentation Academy discourse]: https://discourse.ubuntu.com/c/community/open-documentation-academy/166

[chisel]: https://github.com/canonical/chisel
[chisel-docs]: https://github.com/canonical/chisel-docs
[chisel-releases]: https://github.com/canonical/chisel-releases
