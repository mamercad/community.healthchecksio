from __future__ import absolute_import, division, print_function

__metaclass__ = type

import pytest
from http import HTTPStatus
from mock import patch, MagicMock

from ansible_collections.community.healthchecksio.plugins.module_utils.healthchecksio import (
    HealthchecksioHelper,
    BadgesInfo,
    ChannelsInfo,
    ChecksFlipsInfo,
    ChecksInfo,
    ChecksPingsInfo,
)


class AnsibleExitJson(Exception):
    """
    Exception class to be raised by module.exit_json and caught by the test case

    This prevents the method continuing when it would usually exit
    """
    pass


class AnsibleFailJson(Exception):
    """
    Exception class to be raised by module.fail_json and caught by the test case

    This prevents the method continuing when it would usually exit
    """
    pass


class TestHealthchecksioModuleUtil:
    def test_healthchecksio(self):
        assert True


class ResourceTests:

    @property
    def resource_class(self):
        raise NotImplementedError()

    def setup_method(self):
        self._module = MagicMock()
        self._module.fail_json.side_effect = AnsibleFailJson
        self._module.exit_json.side_effect = AnsibleExitJson
        self._setupModule()

        # Patch the helper to avoid an auth error
        with patch('ansible_collections.community.healthchecksio.plugins.module_utils.healthchecksio.HealthchecksioHelper') as mockHelper:
            self._hcHelper = mockHelper
            self._resource = self.resource_class(self._module)
            self._resource.rest = self._hcHelper

        self._hcHelper.reset_mock()
        self._setupHelper()

    def _setupModule(self, module_params=None, check_mode=False):
        module_params = module_params if module_params else {}

        self._module.params = module_params
        self._module.check_mode = check_mode

    def _setupHelper(self, response_json=None, status_code=HTTPStatus.OK):
        response_json = response_json if response_json else {}

        self._hcHelper.get.return_value.json = response_json
        self._hcHelper.get.return_value.status_code = status_code

    def _assertModuleFail(self, expected_msg):
        self._module.fail_json.assert_called_once_with(changed=False, msg=expected_msg)
        self._module.exit_json.assert_not_called()

    def _assertModuleExit(self, expected_data=None):
        expected_data = expected_data if expected_data else {}

        self._module.exit_json.assert_called_once_with(changed=False, data=expected_data)
        self._module.fail_json.assert_not_called()


class SimpleResourceTests(ResourceTests):
    '''
    Base class for testing simple resources which do not have any parameters and passthrough response data.

    Includes 3 tests which are used for all inheriting classes.
    '''

    @property
    def expected_url(self):
        raise NotImplementedError()

    def test_get_whenErrorStatus(self):
        # Setup
        self._setupHelper(status_code=HTTPStatus.BAD_REQUEST)

        # Run
        try:
            result = self._resource.get()
        except AnsibleFailJson:
            pass

        # Assertions
        self._hcHelper.get.assert_called_with(self.expected_url)
        self._assertModuleFail("Failed to get {} [HTTP 400: (empty error message)]".format(self.expected_url))

    def test_get_whenSuccessful(self):
        # Setup
        response_json = {
            'test': 'value'
        }
        self._setupHelper(response_json)

        # Run
        try:
            result = self._resource.get()
        except AnsibleExitJson:
            pass

        # Assertions
        self._hcHelper.get.assert_called_with(self.expected_url)
        self._assertModuleExit(response_json)

    def test_get_whenCheckMode(self):
        # Setup
        self._setupModule(check_mode=True)

        # Run
        try:
            result = self._resource.get()
        except AnsibleExitJson:
            pass

        # Assertions
        self._hcHelper.get.assert_not_called()
        self._assertModuleExit()


class CheckSubResourceTests(ResourceTests):
    '''
    Base class for testing sub-resources of checks (e.g. pings and flips)
    '''
    _UUIDS = [
        '00000000-0000-0000-0000-000000000000',
        'dfa582de-caa3-447f-9d02-7c481c80408c',
    ]

    @property
    def expected_sub_url(self):
        raise NotImplementedError()

    def _get_expected_url(self, uuid):
        return "checks/{}/{}".format(uuid, self.expected_sub_url)


    @pytest.mark.parametrize("uuid", _UUIDS)
    def test_get_whenErrorStatus(self, uuid):
        # Setup
        self._setupHelper(status_code=HTTPStatus.BAD_REQUEST)
        self._setupModule({ 'uuid': uuid })

        # Run
        try:
            result = self._resource.get()
        except AnsibleFailJson:
            pass

        # Assertions
        expected_url = self._get_expected_url(uuid)
        self._hcHelper.get.assert_called_with(expected_url)
        self._assertModuleFail("Failed to get {} [HTTP 400: (empty error message)]".format(expected_url))

    @pytest.mark.parametrize("uuid", _UUIDS)
    def test_get_whenSuccessful(self, uuid):
        # Setup
        response_json = {
            'test': 'value'
        }
        self._setupHelper(response_json)
        self._setupModule({ 'uuid': uuid })

        # Run
        try:
            result = self._resource.get()
        except AnsibleExitJson:
            pass

        # Assertions
        self._hcHelper.get.assert_called_with(self._get_expected_url(uuid))
        self._assertModuleExit(response_json)

    def test_get_whenCheckMode(self):
        # Setup
        self._setupModule(check_mode=True)

        # Run
        try:
            result = self._resource.get()
        except AnsibleExitJson:
            pass

        # Assertions
        self._hcHelper.get.assert_not_called()
        self._assertModuleExit()


class TestBadgesInfo(SimpleResourceTests):

    @property
    def resource_class(self):
        return BadgesInfo

    @property
    def expected_url(self):
        return 'badges'


class TestChannelsInfo(SimpleResourceTests):

    @property
    def resource_class(self):
        return ChannelsInfo

    @property
    def expected_url(self):
        return 'channels'


class TestChecksFlipsInfo(CheckSubResourceTests):

    @property
    def resource_class(self):
        return ChecksFlipsInfo

    @property
    def expected_sub_url(self):
        return 'flips'


class TestChecksPingsInfo(CheckSubResourceTests):

    @property
    def resource_class(self):
        return ChecksPingsInfo

    @property
    def expected_sub_url(self):
        return 'pings'


class TestChecksInfo(ResourceTests):

    @property
    def resource_class(self):
        return ChecksInfo

    def test_get_whenErrorStatus(self):
        # Setup
        self._setupHelper(status_code=HTTPStatus.BAD_REQUEST)

        # Run
        try:
            result = self._resource.get()
        except AnsibleFailJson:
            pass

        # Assertions
        self._hcHelper.get.assert_called_with('checks')
        self._assertModuleFail("Failed to get checks [HTTP 400]")

    @pytest.mark.parametrize(
        "tags,uuid,expected_url",
        [
            (None, None, 'checks'),
            (['a'], None, 'checks?tag=a'),
            (['a', 'b', 'c'], None, 'checks?tag=a&tag=b&tag=c'),
            (None, '12345', 'checks/12345'),
        ]
    )
    def test_get_whenSuccessful(self, tags, uuid, expected_url):
        # Setup
        self._setupModule({
            'tags': tags,
            'uuid': uuid
        })

        response_json = {
            'test': 'value'
        }
        self._setupHelper(response_json)

        # Run
        try:
            result = self._resource.get()
        except AnsibleExitJson:
            pass

        # Assertions
        self._hcHelper.get.assert_called_with(expected_url)
        self._assertModuleExit(response_json)

    def test_get_whenCheckMode(self):
        # Setup
        self._setupModule(check_mode=True)

        # Run
        try:
            result = self._resource.get()
        except AnsibleExitJson:
            pass

        # Assertions
        self._hcHelper.get.assert_not_called()
        self._assertModuleExit()

    def test_get_whenTagsAndUuidPresent(self):
        # Setup
        self._setupModule({
            'tags': ['a'],
            'uuid': '12345'
        })

        # Run
        try:
            result = self._resource.get()
        except AnsibleFailJson:
            pass

        # Assertions
        self._hcHelper.get.assert_not_called()
        self._assertModuleFail("tags and uuid arguments are mutually exclusive and cannot both be provided.")
