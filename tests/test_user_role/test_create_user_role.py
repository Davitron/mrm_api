import sys
import os
sys.path.append(os.getcwd())

from graphene.test import Client

from tests.base import BaseTestCase
from fixtures.user_role.user_role_fixtures import (
    user_role_mutation_query, user_role_mutation_response
)
from helpers.database import db_session
from api.role.models import Role
from api.user.models import User


class TestCreateUserRole(BaseTestCase):

    def test_user_role_creation(self):
        """
        Testing for User Role creation
        """ 
        user = User(email="info@andela.com")
        user.save()
        role = Role(role="Admin")
        role.save()
        db_session().commit()
        
        execute_query = self.client.execute(
            user_role_mutation_query,
            context_value={'session': db_session})
        
        expected_responese = user_role_mutation_response
        self.assertEqual(execute_query, expected_responese)
