import json
import boto3



#https://www.python.org/doc/essays/graphs/
def find_shortest_path(graph, start, end, path=[]):
        path = path + [start]
        if start == end:
            return path
        if not start in graph:
            return None
        shortest = None
        for node in graph[start]:
            if node not in path:
                newpath = find_shortest_path(graph, node, end, path)
                if newpath:
                    if not shortest or len(newpath) < len(shortest):
                        shortest = newpath
        return shortest
        

def calcDistance(fromCity,toCity,graph):
    shortest_route = find_shortest_path(graph, fromCity, toCity)
    distance = shortest_route.index(toCity) - shortest_route.index(fromCity)
    return distance
    


def lambda_handler(event, context):
    # TODO implement
    
    graph = event

    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('CalcDistance')
    

    # print('received request: ' + str(event))
    req_fromCity = event['currentIntent']['slots']['fromCity'] 
    req_toCity = event['currentIntent']['slots']['toCity'] 
    
    
    # result = table.get_item(Key={'Source': req_fromCity, 'Destination': req_toCity})
    result = calcDistance(req_fromCity,req_toCity,graph)
    print(result)
    
    # distance = result['Item']['Distance']
    
    
    response = {
        "dialogAction": {
            "type": "Close",
            "fulfillmentState": "Fulfilled",
            "message": {
                "contentType": "SSML",
                "content": result
            },
        }
    }
    
    return response
