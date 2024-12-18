# Healthchecks.io Community Collection

[![coverage](https://img.shields.io/codecov/c/github/ansible-collections/community.healthchecksio)](https://codecov.io/gh/ansible-collections/community.healthchecksio)
[![black](https://github.com/ansible-collections/community.healthchecksio/actions/workflows/black.yml/badge.svg)](https://github.com/ansible-collections/community.healthchecksio/actions/workflows/black.yml)
[![integration](https://github.com/ansible-collections/community.healthchecksio/actions/workflows/ansible-test-integration.yml/badge.svg)](https://github.com/ansible-collections/community.healthchecksio/actions/workflows/ansible-test-integration.yml)
[![sanity](https://github.com/ansible-collections/community.healthchecksio/actions/workflows/ansible-test-sanity.yml/badge.svg)](https://github.com/ansible-collections/community.healthchecksio/actions/workflows/ansible-test-sanity.yml)
[![unit](https://github.com/ansible-collections/community.healthchecksio/actions/workflows/ansible-test-unit.yml/badge.svg)](https://github.com/ansible-collections/community.healthchecksio/actions/workflows/ansible-test-unit.yml)

This Ansible collection contains modules for assisting in the automation of the [Healthchecks.io](https://healthchecks.io/) monitoring service. To learn more about this service, please read [https://healthchecks.io/about/](https://healthchecks.io/about/).

From their site:
> Healthchecks.io is an online service for monitoring regularly running tasks such as cron jobs. It uses the Dead man's switch technique: the monitored system must "check in" with Healthchecks.io at regular, configurable time intervals. When Healthchecks.io detects a missed check-in, it sends out alerts.

The service documentation is located at [https://healthchecks.io/docs/](https://healthchecks.io/docs/) and the API documentation is located at [https://healthchecks.io/docs/api/](https://healthchecks.io/docs/api/). This Ansible module strives for API parity.

## Code of Conduct

We follow the [Ansible Code of Conduct](https://docs.ansible.com/ansible/devel/community/code_of_conduct.html) in all our interactions within this project.

If you encounter abusive behavior, please refer to the [policy violations](https://docs.ansible.com/ansible/devel/community/code_of_conduct.html#policy-violations) section of the Code for information on how to raise a complaint.

## Communication

<!--List available communication channels. In addition to channels specific to your collection, we also recommend to use the following ones.-->

<!--We announce releases and important changes through Ansible's [The Bullhorn newsletter](https://github.com/ansible/community/wiki/News#the-bullhorn). Be sure you are [subscribed](https://eepurl.com/gZmiEP).

Join us in the `#ansible` (general use questions and support), `#ansible-community` (community and collection development questions), and other [IRC channels](https://docs.ansible.com/ansible/devel/community/communication.html#irc-channels).-->

Join us in the `#ansible-healthchecksio` channel of [Libera Chat](https://libera.chat/).

We take part in the global quarterly [Ansible Contributor Summit](https://github.com/ansible/community/wiki/Contributor-Summit) virtually or in-person. Track [The Bullhorn newsletter](https://eepurl.com/gZmiEP) and join us.

For more information about communication, refer to the [Ansible Communication guide](https://docs.ansible.com/ansible/devel/community/communication.html).

## Contributing to this collection

<!--Describe how the community can contribute to your collection. At a minimum, fill up and include the CONTRIBUTING.md file containing how and where users can create issues to report problems or request features for this collection. List contribution requirements, including preferred workflows and necessary testing, so you can benefit from community PRs. If you are following general Ansible contributor guidelines, you can link to - [Ansible Community Guide](https://docs.ansible.com/ansible/devel/community/index.html). List the current maintainers (contributors with write or higher access to the repository). The following can be included:-->

The content of this collection is made by people like you, a community of individuals collaborating on making the world better through developing automation software.

We are actively accepting new contributors.

Any kind of contribution is very welcome.

You don't know how to start? Refer to our [contribution guide](CONTRIBUTING.md)!

We use the following guidelines:

* [CONTRIBUTING.md](CONTRIBUTING.md)
* [REVIEW_CHECKLIST.md](REVIEW_CHECKLIST.md)
* [Ansible Community Guide](https://docs.ansible.com/ansible/latest/community/index.html)
* [Ansible Development Guide](https://docs.ansible.com/ansible/devel/dev_guide/index.html)
* [Ansible Collection Development Guide](https://docs.ansible.com/ansible/devel/dev_guide/developing_collections.html#contributing-to-collections)

## Collection maintenance

The current maintainers are listed in the [MAINTAINERS](MAINTAINERS) file. If you have questions or need help, feel free to mention them in the proposals.

To learn how to maintain / become a maintainer of this collection, refer to the [Maintainer guidelines](MAINTAINING.md).

## Governance

<!--Describe how the collection is governed. Here can be the following text:-->

The process of decision making in this collection is based on discussing and finding consensus among participants.

Every voice is important. If you have something on your mind, create an issue or dedicated discussion and let's discuss it!

## Tested with Ansible

<!-- List the versions of Ansible the collection has been tested with. Must match what is in galaxy.yml. -->

Tested with the current Ansible 2.9 and 2.10 releases and the current development version of Ansible.
Ansible versions before 2.9.10 are not supported.

## External requirements

<!-- List any external resources the collection depends on, for example minimum versions of an OS, libraries, or utilities. Do not list other Ansible collections here. -->

An account (and API token) for [Healthchecks.io](https://healthchecks.io/).

### Supported connections
<!-- Optional. If your collection supports only specific connection types (such as HTTPAPI, netconf, or others), list them here. -->

N/A

## Included content

<!-- Galaxy will eventually list the module docs within the UI, but until that is ready, you may need to either describe your plugins etc here, or point to an external docsite to cover that information. -->

### Modules

#### Management API

* `community.healthchecksio.badges_info` - Returns a map of all tags in the project, with badge URLs for each tag.
* `community.healthchecksio.channels_info` - Returns a list of integrations belonging to the project.
* `community.healthchecksio.checks_flips_info` - Get a list of check's status changes.
* `community.healthchecksio.checks_info` - Returns a list of checks belonging to the user, optionally filtered by one or more tags.
* `community.healthchecksio.checks_pings_info` - Returns a list of pings this check has received.
* `community.healthchecksio.checks` - Create, delete, update, and pause checks.

#### Ping API

* `community.healthchecksio.ping` - Signal success, fail, and start events.

## Using this collection

<!--Include some quick examples that cover the most common use cases for your collection content. It can include the following examples of installation and upgrade (change NAMESPACE.COLLECTION_NAME correspondingly):-->

### Management API

```yaml
- name: Get the project badges
  community.healthchecksio.badges_info:
    state: present
    api_key: "{{ api_key }}"
```

```yaml
- name: Get a list of integrations
  community.healthchecksio.channels_info:
    state: present
    api_key: "{{ api_key }}"
```

```yaml
- name: Create a check named "test"
  community.healthchecksio.checks:
    state: present
    api_key: "{{ api_key }}"
    name: test
    unique: ["name"]
```

```yaml
- name: Create a check named "test hourly"
  community.healthchecksio.checks:
    state: present
    api_key: "{{ api_key }}"
    name: "test hourly"
    unique: ["name"]
    tags: ["test", "hourly"]
    desc: "my hourly test check"
    schedule: "0 * * * *"
```

```yaml
- name: Returns all of the checks
  community.healthchecksio.checks_info:
    state: present
    api_key: "{{ api_key }}"
```

```yaml
- name: Pause a check by uuid
  community.healthchecksio.checks:
    state: pause
    api_key: "{{ api_key }}"
    uuid: "{{ check_uuid }}"
```

```yaml
- name: Delete a check by uuid
  community.healthchecksio.checks:
    state: absent
    api_key: "{{ api_key }}"
    uuid: "{{ check_uuid }}"
```

```yaml
- name: Get a list of checks pings
  community.healthchecksio.checks_pings_info:
    state: pings
    api_key: "{{ api_key }}"
    uuid: "{{ check_uuid }}"
```

```yaml
- name: Get a list of checks flips
  community.healthchecksio.checks_flips_info:
    state: flips
    api_key: "{{ api_key }}"
    uuid: "{{ check_uuid }}"
```

### Ping API

```yaml
- name: Send a success signal
  community.healthchecksio.ping:
    state: present
    uuid: "{{ check_uuid }}"
    signal: success
```

```yaml
- name: Send a fail signal
  community.healthchecksio.ping:
    state: present
    uuid: "{{ check_uuid }}"
    signal: fail
```

```yaml
- name: Send a start signal
  community.healthchecksio.ping:
    state: present
    uuid: "{{ check_uuid }}"
    signal: start
```

### Using a self-hosted instance of Healthchecks.io

The `management_api_base_url` and `ping_api_base_url` parameters can be used to direct the modules in this Collection towards a self-hosted instance of Healthchecks.io. By default, or if unset, it defaults to the public instance located at hc-ping.com.

Example Ansible configuration using the `management_api_base_url` and `ping_api_base_url` variables:

```yaml
- name: Create a check named "test"
  community.healthchecksio.checks:
    state: present
    api_key: "{{ api_key }}"
    management_api_base_url: "{{ management_api_base_url }}"
    ping_api_base_url: "{{ ping_api_base_url }}"
    name: test
    unique: ["name"]
```

### Installing the Collection from Ansible Galaxy

Before using this collection, you need to install it with the Ansible Galaxy command-line tool:
```bash
ansible-galaxy collection install community.healthchecksio
```

You can also include it in a `requirements.yml` file and install it with `ansible-galaxy collection install -r requirements.yml`, using the format:
```yaml
---
collections:
  - name: community.healthchecksio
```

Note that if you install the collection from Ansible Galaxy, it will not be upgraded automatically when you upgrade the `ansible` package. To upgrade the collection to the latest available version, run the following command:
```bash
ansible-galaxy collection install community.healthchecksio --upgrade
```

You can also install a specific version of the collection, for example, if you need to downgrade when something is broken in the latest version (please report an issue in this repository). Use the following syntax to install version `0.1.0`:

```bash
ansible-galaxy collection install community.healthchecksio
```

See [Ansible Using collections](https://docs.ansible.com/ansible/devel/user_guide/collections_using.html) for more details.

## Release notes

See the [changelog](https://github.com/ansible-collections/REPONAMEHERE/tree/main/CHANGELOG.rst).

## Roadmap

<!-- Optional. Include the roadmap for this collection, and the proposed release/versioning strategy so users can anticipate the upgrade/update cycle. -->

There's a pinboard issue [here](https://github.com/ansible-collections/community.healthchecksio/issues/2) and we can have discussions [here](https://github.com/ansible-collections/community.healthchecksio/discussions).

## More information

<!-- List out where the user can find additional information, such as working group meeting times, slack/IRC channels, or documentation for the product this collection automates. At a minimum, link to: -->

- [Ansible Collection overview](https://github.com/ansible-collections/overview)
- [Ansible User guide](https://docs.ansible.com/ansible/devel/user_guide/index.html)
- [Ansible Developer guide](https://docs.ansible.com/ansible/devel/dev_guide/index.html)
- [Ansible Collections Checklist](https://github.com/ansible-collections/overview/blob/master/collection_requirements.rst)
- [Ansible Community code of conduct](https://docs.ansible.com/ansible/devel/community/code_of_conduct.html)
- [The Bullhorn (the Ansible Contributor newsletter)](https://us19.campaign-archive.com/home/?u=56d874e027110e35dea0e03c1&id=d6635f5420)
- [Changes impacting Contributors](https://github.com/ansible-collections/overview/issues/45)

## Licensing

<!-- Include the appropriate license information here and a pointer to the full licensing details. If the collection contains modules migrated from the ansible/ansible repo, you must use the same license that existed in the ansible/ansible repo. See the GNU license example below. -->

GNU General Public License v3.0 or later.

See [LICENSE](https://www.gnu.org/licenses/gpl-3.0.txt) to see the full text.
