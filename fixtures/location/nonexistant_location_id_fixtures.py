query_nonexistant_location_id = '''{
getRoomsInALocation(locationId:4){
    name
    abbreviation
    office{
        buildingName
        blocks {
            name
            floors {
                name
                rooms {
                    capacity
                    name
                    roomType
                }
            }
        }
    }
    }
}
'''

expected_query_with_nonexistant_id = {
    "data": {
        "getRoomsInALocation": []
    }
}
