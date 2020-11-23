from regex_matchers import retrieve_exceptions, check_for_java
from stack_exchange import get_stackoverflow_links, format_stackoverflow_query_string
import json
from flask import Flask, Response, request

def get_links(input_stack_trace):
    if not check_for_java(input_stack_trace):
        print("Not a java stack trace")
        exit()

    exceptions = retrieve_exceptions(input_stack_trace)
    if len(exceptions) == 0:
        print("No exceptions found")
        exit()

    cause_exception = exceptions[-1]
    queries = format_stackoverflow_query_string(cause_exception.exception, cause_exception.message)

    result = []
    for query in queries:
        if len(result) >= 5:
            break

        result.extend(get_stackoverflow_links(query, ["java"])["items"])
        result = result[0:5]

    for query in queries:
        if len(result) >= 5:
            break

        result.extend(get_stackoverflow_links(query)["items"])
        result = result[0:5]

    top_results = []
    dump = {"results": top_results}
    for i in result:
        top_results.append({
            "Link": i["link"],
            "Title": i['title'],
            "Score": i['score']
        })

    return dump

api = Flask(__name__)

@api.route('/', methods=['GET'])
def get_example():
    example_request = '''
        Exception in thread "main" java.lang.NumberFormatException: For input string: "30k"
            at java.lang.NumberFormatException.forInputString(NumberFormatException.java:65)
            at java.lang.Integer.parseInt(Integer.java:580)
            at java.lang.Integer.parseInt(Integer.java:615)
            at NumberFormatExceptionTest.main(NumberFormatExceptionTest.java:3)
    '''

    dump = get_links(example_request)
    return Response(json.dumps(dump), mimetype='application/json')


@api.route('/', methods=['POST'])
def get_posted_links():
    dump = get_links(request.get_json()["stack"])
    return Response(json.dumps(dump), mimetype='application/json')

if __name__ == '__main__':
    api.run()
