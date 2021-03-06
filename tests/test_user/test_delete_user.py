import sys
import os
import json

from tests.base import BaseTestCase
from fixtures.user.delete_user import (
    delete_user, expected_query_after_delete, delete_self, user_not_found)
from fixtures.token.token_fixture import (admin_api_token, user_api_token)
from api.user.models import User
from api.role.models import Role
from api.user_role.models import UsersRole

sys.path.append(os.getcwd())


class TestDeleteUser(BaseTestCase):
    def test_deleteuser_when_not_admin(self):
        api_headers = {'token': user_api_token}
        response = self.app_test.post('/mrm?query='+delete_user,
                                      headers=api_headers)
        self.assertIn("You are not authorized to perform this action",
                      str(response.data))

    def test_deleteuser_when_admin(self):
        user = User(email="test.test@andela.com",
                    location="Lagos")
        user.save()
        role = Role(role="Default User")
        role.save()
        user_role = UsersRole(user_id=user.id,
                              role_id=role.id)
        user_role.save()
        api_headers = {'token': admin_api_token}
        response = self.app_test.post('/mrm?query='+delete_user,
                                      headers=api_headers)
        expected_response = expected_query_after_delete
        self.assertEquals(json.loads(response.data), expected_response)

    def test_user_delete_admin(self):
        admin_user = User(email="new.user@andela.com",
                          location="Kampala")
        admin_user.save()
        user_role = UsersRole(user_id=admin_user.id, role_id=1)
        user_role.save()
        api_headers = {'token': admin_api_token}
        response = self.app_test.post('/mrm?query='+delete_user,
                                      headers=api_headers)
        expected_response = "You are not authorized to delete an Admin"
        actual_response = json.loads(response.data)
        self.assertIn(expected_response,
                      actual_response["errors"][0]["message"])

    def test_delete_self(self):
        api_headers = {'token': admin_api_token}
        response = self.app_test.post('/mrm?query='+delete_self,
                                      headers=api_headers)
        expected_response = "You cannot delete yourself"
        actual_response = json.loads(response.data)
        self.assertIn(expected_response,
                      actual_response["errors"][0]["message"])

    def test_deleteuser_not_found(self):
        api_headers = {'token': admin_api_token}
        response = self.app_test.post('/mrm?query='+user_not_found,
                                      headers=api_headers)
        expected_response = "User not found"
        actual_response = json.loads(response.data)
        self.assertIn(expected_response,
                      actual_response["errors"][0]["message"])
