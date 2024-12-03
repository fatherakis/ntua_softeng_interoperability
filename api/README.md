# REST-API

## Base URL
https://{host}:9103/interoperability/api

## Supports json and csv 
by query parameter: _{baseURL}/{service}/{path-to-resource}?format={json|csv}_

## (Optional) User authentication. 
User accounts are created by the admin through the use of the CLI. Authentication tokens will be provided in a custom HTTP header: X-OBSERVATORY-AUTH 

## HTTP Error handling
|     |                       |                              |
| --- | --------------------- | ---------------------------- |
| 200 | Success               | Successfull call             |
| 400 | Bad request           | Invalid parameters in a call |
| 401 | Not authorized        | Request by unauthorized user |
| 402 | No data               | Request reply is null        |
| 500 | Internal server error | Any other error              |



## Endpoints

### (Optional) Login & logout

1.  **{baseURL}/login**    
Supports POST method and receives the username & password parameters of the user encoded  as "application/x-www-form-urlencoded". In a successfull authentication use case a json object with the token is returned (example: {"token":"FOO"})

2. **{baseURL}/logout**    
Supports POST method, doesn't receive any parameters (the user's token is decoupled and is included in the special purpose HTTP header that was declared earlier). In a successfull call status code 200 is returned (no body).


### Administration endpoints

1. **{baseURL}/admin/healthcheck**    
Supports GET method and confirms end-to-end connectivity between the user and the database. More specifically the backend checks the DB connectivity and responds. In a successfull connection the json object {"status":"OK", "dbconnection":[connection string]} is returned, else {"status":"failed", "dbconnection":[connection string]} is returned. The connection string includes DB-specific info.

2. **{baseURL}/admin/resetpasses**    
Supports POST method and proceeds to initialize the Passes table (deletion of every instance). Also if user authentication is implemented, the default admin account is created. In a successfull call the json object {"status":"OK"} is returned, else {"status":"failed"}.

3. **{baseURL}/admin/resetstations**    
Supports POST method and proceeds to initialize the Stations table with the default instances. In a successfull call the json object {"status":"OK"} is returned, else {"status":"failed"} (with optional failure description).

4. **{baseURL}/admin/resetvehicles**    
Supports POST method and proceeds to initialize the Vehicles table with the default instances. In a successfull call the json object {"status":"OK"} is returned, else {"status":"failed"} (with optional failure description).


### Functional endpoints

1. **{baseURL}/PassesPerStation/:stationID/:date_from/:date_to**    
A list of the Passes data for the station and the time period specified. The date format returned is: "YYYY-MM-DD HH:MM:SS"

| Field            | Type    | Description                              |
| ---------------- | ------- | ---------------------------------------- |
| Station          | String  | Unique ID of pass point                  |                 
| StationOperator  | String  | The toll station admin                   |
| RequestTimestamp | String  | Date/time of endpoint call               |
| PeriodFrom       | String  | Requested period beginning               |
| PeriodTo         | String  | Requested period ending                  |
| NumberOfPasses   | Integer | Number of passes in the period           |
| PassesList:      | List    | Includes [NumberOfPasses] elements       |
| PassIndex        | Integer | Index (increasing) of pass in the period |
| PassID           | String  | ID of pass instance                      |
| PassTimeStamp    | String  | Pass timestamp                           |              
| VehicleID        | String  | ID of vehicle                            |             
| TagProvider      | String  | Tag provider of the vehicle tag          |            
| PassType         | String  | "home" or "visitor"                      |    
| PassCharge       | Float   | Charge for passing                       |
                                                                          
   --------------------------------------------------------                                                                          
                                                                          

2. **{baseURL}/PassesAnalysis/:op1_ID/:op2_ID/:date_from/:date_to**    
A list of the Passes data in stations of OP1_ID by vehicles with tag of OP2_ID. Every pass is of PassType "visitor" in the PassesPerStation call. The date format returned is: "YYYY-MM-DD HH:MM:SS"

| Field            | Type    | Description                              |
| ---------------- | ------- | ---------------------------------------- |
| OP1_ID           | String  | operator1 ID                             |                 
| OP2_ID           | String  | operator2 ID                             |
| RequestTimestamp | String  | Date/time of endpoint call               |
| PeriodFrom       | String  | Requested period beginning               |
| PeriodTo         | String  | Requested period ending                  |
| NumberOfPasses   | Integer | Number of passes in the period           |
| PassesList:      | List    | Includes [NumberOfPasses] elements       |
| PassIndex        | Integer | Index (increasing) of pass in the period |
| PassID           | String  | ID of pass instance                      |
| PassTimeStamp    | String  | Pass timestamp                           |              
| VehicleID        | String  | ID of vehicle                            |             
| Charge           | Float   | Charge for passing                       |
                                                                          
   ------------------------------------------------------                                                                          
                                                                          

3. **{baseURL}/PassesCost/:op1_ID/:op2_ID/:date_from/:date_to**    
Returns the number of Pass instances by Vehicles with tag provided by OP2_ID in stations of OP1_ID, as well as the total cost of those, in the requested period. 

| Field            | Type    | Description                    |
| ---------------- | ------- | ------------------------------ |
| OP1_ID           | String  | operator1 ID                   |                 
| OP2_ID           | String  | operator2 ID                   |
| RequestTimestamp | String  | Date/time of endpoint call     |
| PeriodFrom       | String  | Requested period beginning     |
| PeriodTo         | String  | Requested period ending        |
| NumberOfPasses   | Integer | Number of passes in the period |
| PassesCost       | Float   | The total cost of the passes   |
                                                                          
   -----------------------------------------------------                                                                          
                                                                          

4. **{baseURL}/ChargesBy/:op_ID/:date_from/:date_to**    
Returns the number of Pass instances in stations of OP1_ID by "visitor" Vehicles, as well as the total cost of each visitor tag provider, in the requested period. 

| Field            | Type    | Description                                                                                                 |
| ---------------- | ------- | ----------------------------------------------------------------------------------------------------------- |
| OP1_ID           | String  | operator1 ID                                                                                                |
| OP2_ID           | String  | operator2 ID                                                                                                |
| RequestTimestamp | String  | Date/time of endpoint call                                                                                  |
| PeriodFrom       | String  | Requested period beginning                                                                                  |
| PeriodTo         | String  | Requested period ending                                                                                     |
| PPOList:         | List    | Includes as many elements as the distinct operators which cars' passes by the OP1_ID stations in the period |
| NumberOfPasses   | Integer | Number of passes in the period                                                                              |
| PassesCost       | Float   | The total cost of the passes                                                                                |
