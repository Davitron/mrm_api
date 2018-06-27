all_locations_query = '''
{
  allLocations{
    name
    abbreviation
    offices{
      buildingName
      blocks{
        name
        floors{
          name
          rooms{
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


expected_query_all_locations = {
  "data": {
    "allLocations": [
      {
        "name": "Uganda",
        "abbreviation": "KLA",
        "offices": [
          {
            "buildingName": "EPIC Tower",
            "blocks": [{
                "name": "EC",
                "floors": [{
                    "name": "3rd",
                    "rooms": [{
                        "capacity": 6,
                        "name": "Entebbe",  # noqa: E501
                        "roomType": "meeting"  # noqa: E501
                    }]
                }]
            }]
          }
        ]
      }
    ]
  }
}


pass_an_arg_all_locations = '''
    {
        allLocations(locationId: 1){
            name
            abbreviation
            offices{
            buildingName
            blocks{
                name
                floors{
                name
                rooms{
                    capacity
                    name
                    roomType
                }
                }
            }
            }
        }
    }'''

expected_response_pass_an_arg = {
                                    "errors": [
                                        {
                                        "message": "Unknown argument \"locationId\" on field \"allLocations\" of type \"Query\".",  # noqa: E501
                                        "locations": [
                                            {
                                                "line": 3,
                                                "column": 22
                                                        }
                                                        ]
                                                        }
                                                        ]
                                                        }

all_location_no_hierachy = '''{
    allLocations{
        rooms {
            name
            roomType
            capacity
        }
    }
}'''
expected_all_location_no_hierachy = {
    "errors": [
            {
                "message": "Cannot query field \"rooms\" on type \"Location\".",  # noqa: E501
                "locations": [
                    {
                        "line": 3,
                        "column": 9
                    }
                ]
            }
        ]
    }
