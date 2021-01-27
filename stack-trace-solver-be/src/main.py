from regex_matchers import retrieve_exceptions, check_for_java
from stack_exchange import get_stackoverflow_links, format_stackoverflow_query_string
import json
from flask import Flask, Response, request
from flask_cors import CORS, cross_origin

def get_links(generated_queries, tags):
    result = []
    for generated_query in generated_queries:
        if len(result) >= 5:
            break

        for query in generated_query.queries:
            responses = get_stackoverflow_links(query, tags)["items"]
            for response in responses:
                result.append((generated_query.template, response, query))

        result = result[0:5]
    
    return result

def generate_results(input_stack_trace):
    if not check_for_java(input_stack_trace):
        return { "results": [], "error": "Not a java stack trace" }

    exceptions = retrieve_exceptions(input_stack_trace)
    if len(exceptions) == 0:
        return { "results": [], "error": "No exceptions found" }

    cause_exception = exceptions[-1]
    generated_queries = format_stackoverflow_query_string(cause_exception.exception, cause_exception.message)

    result = get_links(generated_queries, ["java"])

    if (len(result) < 5):
        result.extend(get_links(generated_queries, []))
        result = result[0:5]

    top_results = []
    dump = {"results": top_results}
    for i in result:
        template, response, query = i
        top_results.append({
            "GeneratedQuery": query,
            "DetectedException": cause_exception.__str__(),
            "Template": template,
            "Link": response["link"],
            "Title": response['title'],
            "Score": response['score']
        })

    return dump

api = Flask(__name__)
CORS(api)

@api.route('/', methods=['GET'])
@cross_origin()
def get_example():
    example_request = '''
        Exception in thread "main" java.lang.NumberFormatException: For input string: "30k"
            at java.lang.NumberFormatException.forInputString(NumberFormatException.java:65)
            at java.lang.Integer.parseInt(Integer.java:580)
            at java.lang.Integer.parseInt(Integer.java:615)
            at NumberFormatExceptionTest.main(NumberFormatExceptionTest.java:3)
    '''

    dump = generate_results(example_request)
    return Response(json.dumps(dump), mimetype='application/json')


@api.route('/', methods=['POST'])
@cross_origin()
def get_posted_links():
    dump = generate_results(request.get_json()["stack"])
    return Response(json.dumps(dump), mimetype='application/json')

if __name__ == '__main__':
    api.run(host="0.0.0.0")
