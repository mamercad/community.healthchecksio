#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2021, Mark Mercado <mamercad@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = r"""
---
module: checks
short_description: Create, delete, update, and pause checks
description:
  - Creates a new check and returns its ping URL.
  - For C(state=absent), will delete the check with the given C(uuid).
  - For C(state=pause), will pause the check with the given C(uuid).
  - All request parameters are optional and will use their default values if omitted.
  - To create a Simple check, specify the C(timeout) parameter.
  - To create a Cron check, specify the C(schedule) and C(tz) parameters.
author: "Mark Mercado (@mamercad)"
version_added: 0.1.0
options:
  state:
    description:
      - C(present) will create or update a check.
      - C(absent) will delete a check.
      - C(pause) will pause a check.
    type: str
    choices: ["present", "absent", "pause"]
    default: present
  name:
    description:
      - Name for the new check.
    type: str
    required: false
    default: ""
  tags:
    description:
      - Tags for the check.
    type: list
    elements: str
    required: false
    default: []
  desc:
    description:
      - Description of the check.
    type: str
    required: false
    default: ""
  timeout:
    description:
      - A number of seconds, the expected period of this check.
      - Minimum 60 (one minute), maximum 2592000 (30 days).
    type: int
    required: false
  grace:
    description:
      - A number of seconds, the grace period for this check.
    type: int
    required: false
    default: 3600
  schedule:
    description:
      - A cron expression defining this check's schedule.
      - If you specify both timeout and schedule parameters, Healthchecks.io will create a Cron check and ignore the timeout value.
    type: str
    required: false
  tz:
    description:
      - Server's timezone. This setting only has an effect in combination with the schedule parameter.
    type: str
    required: false
  manual_resume:
    description:
      - Controls whether a paused check automatically resumes when pinged (the default) or not.
      - If set to false, a paused check will leave the paused state when it receives a ping.
      - If set to true, a paused check will ignore pings and stay paused until you manually resume it from the web dashboard.
    type: bool
    required: false
    default: false
  methods:
    description:
      - Specifies the allowed HTTP methods for making ping requests.
      - Must be one of the two values "" (an empty string) or "POST".
      - Set this field to "" (an empty string) to allow HEAD, GET, and POST requests.
      - Set this field to "POST" to allow only POST requests.
    type: str
    required: false
    default: ""
  channels:
    description:
      - By default, this API call assigns no integrations to the newly created check.
      - Set this field to a special value "*" to automatically assign all existing integrations.
      - To assign specific integrations, use a comma-separated list of integration UUIDs.
    type: str
    required: false
    default: ""
  unique:
    description:
      - Enables "upsert" functionality.
      - Before creating a check, Healthchecks.io looks for existing checks, filtered by fields listed in unique.
      - The accepted values for the unique field are C(name), C(tags), C(timeout), and C(grace).
    type: list
    elements: str
    required: false
    default: []
  uuid:
    description:
      - Check uuid to delete when state is C(absent) or C(pause).
    type: str
    required: false
    default: ""
extends_documentation_fragment:
  - community.healthchecksio.healthchecksio.documentation
"""

EXAMPLES = r"""
- name: Create a Simple check named "test simple"
  community.healthchecksio.checks:
    state: present
    name: "test simple"
    desc: "my simple test check"
    unique: ["name"]
    tags: ["test", "simple"]
    timeout: 60

- name: Create a Cron check named "test hourly"
  community.healthchecksio.checks:
    state: present
    name: "test hourly"
    unique: ["name"]
    tags: ["test", "hourly"]
    desc: "my hourly test check"
    schedule: "0 * * * *"
    tz: UTC
"""

RETURN = r"""
data:
  description: Create, update, pause or delete response
  returned: always
  type: dict
  sample:
    channels: ''
    desc: ''
    grace: 3600
    last_ping: null
    manual_resume: false
    methods: ''
    n_pings: 0
    name: test
    next_ping: null
    pause_url: https://healthchecks.io/api/v1/checks/524d0f69-0ff3-4120-a2e2-03ebd5736b25/pause
    ping_url: https://hc-ping.com/524d0f69-0ff3-4120-a2e2-03ebd5736b25
    schedule: '* * * * *'
    slug: test
    status: new
    tags: ''
    tz: UTC
    update_url: https://healthchecks.io/api/v1/checks/524d0f69-0ff3-4120-a2e2-03ebd5736b25
msg:
  description: Create, update, pause or delete message
  returned: always
  type: str
  sample: New check 524d0f69-0ff3-4120-a2e2-03ebd5736b25 created
uuid:
  description: Check UUID from create or update
  returned: changed
  type: str
  sample: 524d0f69-0ff3-4120-a2e2-03ebd5736b25
"""

from ansible_collections.community.healthchecksio.plugins.module_utils.healthchecksio import (
    HealthchecksioHelper,
    Checks,
)
from ansible.module_utils.basic import AnsibleModule, env_fallback


def run(module):
    state = module.params.pop("state")
    checks = Checks(module)
    if state == "present":
        checks.create()
    elif state == "absent":
        checks.delete()
    elif state == "pause":
        checks.pause()


def main():
    argument_spec = HealthchecksioHelper.healthchecksio_argument_spec()
    argument_spec.update(
        state=dict(
            type="str", choices=["present", "absent", "pause"], default="present"
        ),
        name=dict(type="str", required=False, default=""),
        tags=dict(type="list", elements="str", required=False, default=[]),
        desc=dict(type="str", required=False, default=""),
        timeout=dict(type="int", required=False),
        grace=dict(type="int", required=False, default=3600),
        schedule=dict(type="str", required=False),
        tz=dict(type="str", required=False),
        manual_resume=dict(type="bool", required=False, default=False),
        methods=dict(type="str", required=False, default=""),
        channels=dict(type="str", required=False, default=""),
        unique=dict(type="list", elements="str", required=False, default=[]),
        uuid=dict(type="str", required=False, default=""),
        slug=dict(type="str", required=False, default=""),
    )
    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
        required_if=[("state", "absent", ["uuid"]), ("state", "pause", ["uuid"])],
        required_together=[("schedule", "tz")],
        mutually_exclusive=[("timeout", "schedule"), ("timeout", "tz")],
    )

    run(module)


if __name__ == "__main__":
    main()
