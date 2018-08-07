import graphene

from graphene_sqlalchemy import (SQLAlchemyObjectType)
from graphql import GraphQLError

from api.room.models import Room as RoomModel
from api.office.models import Office
from helpers.calendar.events import RoomSchedules
from utilities.utility import validate_empty_fields, update_entity_fields
from helpers.auth.authentication import Auth
from helpers.auth.verify_ids_for_room import verify_ids
from helpers.auth.check_office_name import assert_wing_is_required
from helpers.auth.add_office import verify_attributes


class Room(SQLAlchemyObjectType):
    class Meta:
        model = RoomModel


class Calendar(graphene.ObjectType):
    events = graphene.String()
    occupants = graphene.String()


class RoomFilter(graphene.ObjectType):
    rooms = graphene.List(Room)
    
    def resolve_rooms(self, info, capacity):
        query = Room.get_query(info)
        if capacity:
            print(capacity)
            return query.filter(RoomModel.capacity.filter_by(capacity)).all()
        # if kwargs.pop("resources", None):
        #     return Room.query.filter(RoomModel.resources.filter_by(kwargs['resources'])).all()



class CreateRoom(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        room_type = graphene.String(required=True)
        capacity = graphene.Int(required=True)
        image_url = graphene.String()
        floor_id = graphene.Int(required=True)
        calendar_id = graphene.String(required=True)
        office_id = graphene.Int()
        wing_id = graphene.Int()
    room = graphene.Field(Room)

    @Auth.user_roles('Admin')
    def mutate(self, info, office_id, **kwargs):
        verify_attributes(kwargs)
        verify_ids(kwargs, office_id)
        get_office = Office.query.filter_by(id=office_id).first()
        assert_wing_is_required(get_office.name, kwargs)
        room = RoomModel(**kwargs)
        room.save()

        return CreateRoom(room=room)


class UpdateRoom(graphene.Mutation):
    class Arguments:
        room_id = graphene.Int()
        name = graphene.String()
        room_type = graphene.String()
        capacity = graphene.Int()
        image_url = graphene.String()
        calendar_id = graphene.String()
    room = graphene.Field(Room)

    @Auth.user_roles('Admin')
    def mutate(self, info, room_id, **kwargs):
        validate_empty_fields(**kwargs)

        query_room = Room.get_query(info)
        exact_room = query_room.filter(RoomModel.id == room_id).first()
        if not exact_room:
            raise GraphQLError("RoomId not found")
        update_entity_fields(exact_room, **kwargs)

        exact_room.save()
        return UpdateRoom(room=exact_room)


class DeleteRoom(graphene.Mutation):

    class Arguments:
        room_id = graphene.Int(required=True)
    room = graphene.Field(Room)

    @Auth.user_roles('Admin')
    def mutate(self, info, room_id, **kwargs):
        query_room = Room.get_query(info)
        exact_room = query_room.filter(
            RoomModel.id == room_id).first()
        if not exact_room:
            raise GraphQLError("RoomId not found")

        exact_room.delete()
        return DeleteRoom(room=exact_room)


class Query(graphene.ObjectType):
    all_rooms = graphene.List(Room)
    get_room_by_id = graphene.Field(
        Room,
        room_id=graphene.Int()
    )
    room_schedule = graphene.Field(
        Calendar,
        calendar_id=graphene.String(),
        days=graphene.Int(),
    )
    room_occupants = graphene.Field(
        Calendar,
        calendar_id=graphene.String(),
        days=graphene.Int(),
    )
    room_filter = graphene.List(
        Room,
        capacity=graphene.Int()
        )

    def resolve_all_rooms(self, info):
        query = Room.get_query(info)
        return query.all()

    def resolve_get_room_by_id(self, info, room_id):
        query = Room.get_query(info)
        check_room = query.filter(RoomModel.id == room_id).first()
        if not check_room:
            raise GraphQLError("Room not found")
        return check_room

    def resolve_room_occupants(self, info, calendar_id, days):
        query = Room.get_query(info)
        check_calendar_id = query.filter(
            RoomModel.calendar_id == calendar_id
        ).first()
        if not check_calendar_id:
            raise GraphQLError("Invalid CalendarId")
        room_occupants = RoomSchedules.get_room_schedules(
            self,
            calendar_id,
            days)
        return Calendar(
            occupants=room_occupants[0]
        )

    def resolve_room_schedule(self, info, calendar_id, days):
        query = Room.get_query(info)
        check_calendar_id = query.filter(
            RoomModel.calendar_id == calendar_id
        ).first()
        if not check_calendar_id:
            raise GraphQLError("CalendarId given not assigned to any room on converge")  # noqa: E501
        room_schedule = RoomSchedules.get_room_schedules(
            self,
            calendar_id,
            days)
        return Calendar(
            events=room_schedule[1]
        )


class Mutation(graphene.ObjectType):
    create_room = CreateRoom.Field()
    update_room = UpdateRoom.Field()
    delete_room = DeleteRoom.Field()
