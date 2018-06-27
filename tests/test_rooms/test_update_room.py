

from tests.base import BaseTestCase

from fixtures.room.room_update_fixtures import (
    query_update_all_fields,
    query_without_room_id,
    query_room_id_non_existant,
    update_with_empty_field
)
from fixtures.token.token_fixture import api_token
from api.user.models import User
from api.role.models import Role
from api.user_role.models import UsersRole


class TestUpdateRoom(BaseTestCase):

    def create_admin(self):
        user = User(email="patrick.walukagga@andela.com",
                    location="Kampala")
        user.save()
        role = Role(role="Admin")
        role.save()
        user_role = UsersRole(user_id=user.id, role_id=role.id)
        user_role.save()
        role = Role(role="Default User")
        role.save()

    def test_resource_update_mutation_when_not_admin(self):

        api_headers = {'token': api_token}
        response = self.app_test.post('/mrm?query='+query_update_all_fields,
                                      headers=api_headers)
        self.assertIn("You are not authorized to perform this action",
                      str(response.data))

    def test_if_all_fields_updated(self):
        self.create_admin()
        api_headers = {'token': api_token}
        response = self.app_test.post('/mrm?query='+query_update_all_fields,
                                      headers=api_headers)
        self.assertIn("Jinja", str(response.data))

    def test_for_error_if_id_not_supplied(self):
        self.create_admin()
        api_headers = {'token': api_token}
        response = self.app_test.post('/mrm?query='+query_without_room_id,
                                      headers=api_headers)
        self.assertIn("required positional argument", str(response.data))

    def test_for_error_if_room_id_is_non_existant_room(self):
        self.create_admin()
        api_headers = {'token': api_token}
        response = self.app_test.post('/mrm?query='+query_room_id_non_existant,
                                      headers=api_headers)
        self.assertIn("RoomId not found", str(response.data))

    def test_update_with_empty_field(self):
        user = User(email="patrick.walukagga@andela.com",
                    location="Kampala")
        user.save()
        role = Role(role="Admin")
        role.save()
        user_role = UsersRole(user_id=user.id, role_id=role.id)
        user_role.save()
        role = Role(role="Default User")
        role.save()
        api_headers = {'token': api_token}
        response = self.app_test.post('/mrm?query='+update_with_empty_field,
                                      headers=api_headers)
        self.assertIn("name is required field", str(response.data))
