from regex_matchers import retrieve_exceptions, check_for_java
from stack_exchange import get_stackoverflow_links, format_stackoverflow_query_string
import json
from flask import Flask, Response, request

input_stack_trace = '''
    javax.servlet.ServletException: Something bad happened
        at com.example.myproject.OpenSessionInViewFilter.doFilter(OpenSessionInViewFilter.java:60)
        at org.mortbay.jetty.servlet.ServletHandler$CachedChain.doFilter(ServletHandler.java:1157)
        at com.example.myproject.ExceptionHandlerFilter.doFilter(ExceptionHandlerFilter.java:28)
        at org.mortbay.jetty.servlet.ServletHandler$CachedChain.doFilter(ServletHandler.java:1157)
        at com.example.myproject.OutputBufferFilter.doFilter(OutputBufferFilter.java:33)
        at org.mortbay.jetty.servlet.ServletHandler$CachedChain.doFilter(ServletHandler.java:1157)
        at org.mortbay.jetty.servlet.ServletHandler.handle(ServletHandler.java:388)
        at org.mortbay.jetty.security.SecurityHandler.handle(SecurityHandler.java:216)
        at org.mortbay.jetty.servlet.SessionHandler.handle(SessionHandler.java:182)
        at org.mortbay.jetty.handler.ContextHandler.handle(ContextHandler.java:765)
        at org.mortbay.jetty.webapp.WebAppContext.handle(WebAppContext.java:418)
        at org.mortbay.jetty.handler.HandlerWrapper.handle(HandlerWrapper.java:152)
        at org.mortbay.jetty.Server.handle(Server.java:326)
        at org.mortbay.jetty.HttpConnection.handleRequest(HttpConnection.java:542)
        at org.mortbay.jetty.HttpConnection$RequestHandler.content(HttpConnection.java:943)
        at org.mortbay.jetty.HttpParser.parseNext(HttpParser.java:756)
        at org.mortbay.jetty.HttpParser.parseAvailable(HttpParser.java:218)
        at org.mortbay.jetty.HttpConnection.handle(HttpConnection.java:404)
        at org.mortbay.jetty.bio.SocketConnector$Connection.run(SocketConnector.java:228)
        at org.mortbay.thread.QueuedThreadPool$PoolThread.run(QueuedThreadPool.java:582)
    Caused by: com.example.myproject.MyProjectServletException
        at com.example.myproject.MyServlet.doPost(MyServlet.java:169)
        at javax.servlet.http.HttpServlet.service(HttpServlet.java:727)
        at javax.servlet.http.HttpServlet.service(HttpServlet.java:820)
        at org.mortbay.jetty.servlet.ServletHolder.handle(ServletHolder.java:511)
        at org.mortbay.jetty.servlet.ServletHandler$CachedChain.doFilter(ServletHandler.java:1166)
        at com.example.myproject.OpenSessionInViewFilter.doFilter(OpenSessionInViewFilter.java:30)
        ... 27 more
    Caused by: org.hibernate.exception.ConstraintViolationException: could not insert: [com.example.myproject.MyEntity]
        at org.hibernate.exception.SQLStateConverter.convert(SQLStateConverter.java:96)
        at org.hibernate.exception.JDBCExceptionHelper.convert(JDBCExceptionHelper.java:66)
        at org.hibernate.id.insert.AbstractSelectingDelegate.performInsert(AbstractSelectingDelegate.java:64)
        at org.hibernate.persister.entity.AbstractEntityPersister.insert(AbstractEntityPersister.java:2329)
        at org.hibernate.persister.entity.AbstractEntityPersister.insert(AbstractEntityPersister.java:2822)
        at org.hibernate.action.EntityIdentityInsertAction.execute(EntityIdentityInsertAction.java:71)
        at org.hibernate.engine.ActionQueue.execute(ActionQueue.java:268)
        at org.hibernate.event.def.AbstractSaveEventListener.performSaveOrReplicate(AbstractSaveEventListener.java:321)
        at org.hibernate.event.def.AbstractSaveEventListener.performSave(AbstractSaveEventListener.java:204)
        at org.hibernate.event.def.AbstractSaveEventListener.saveWithGeneratedId(AbstractSaveEventListener.java:130)
        at org.hibernate.event.def.DefaultSaveOrUpdateEventListener.saveWithGeneratedOrRequestedId(DefaultSaveOrUpdateEventListener.java:210)
        at org.hibernate.event.def.DefaultSaveEventListener.saveWithGeneratedOrRequestedId(DefaultSaveEventListener.java:56)
        at org.hibernate.event.def.DefaultSaveOrUpdateEventListener.entityIsTransient(DefaultSaveOrUpdateEventListener.java:195)
        at org.hibernate.event.def.DefaultSaveEventListener.performSaveOrUpdate(DefaultSaveEventListener.java:50)
        at org.hibernate.event.def.DefaultSaveOrUpdateEventListener.onSaveOrUpdate(DefaultSaveOrUpdateEventListener.java:93)
        at org.hibernate.impl.SessionImpl.fireSave(SessionImpl.java:705)
        at org.hibernate.impl.SessionImpl.save(SessionImpl.java:693)
        at org.hibernate.impl.SessionImpl.save(SessionImpl.java:689)
        at sun.reflect.GeneratedMethodAccessor5.invoke(Unknown Source)
        at sun.reflect.DelegatingMethodAccessorImpl.invoke(DelegatingMethodAccessorImpl.java:25)
        at java.lang.reflect.Method.invoke(Method.java:597)
        at org.hibernate.context.ThreadLocalSessionContext$TransactionProtectionWrapper.invoke(ThreadLocalSessionContext.java:344)
        at $Proxy19.save(Unknown Source)
        at com.example.myproject.MyEntityService.save(MyEntityService.java:59) <-- relevant call (see notes below)
        at com.example.myproject.MyServlet.doPost(MyServlet.java:164)
        ... 32 more
    Caused by: java.sql.SQLException: Violation of unique constraint MY_ENTITY_UK_1: duplicate value(s) for column(s) MY_COLUMN in statement [...]
        at org.hsqldb.jdbc.Util.throwError(Unknown Source)
        at org.hsqldb.jdbc.jdbcPreparedStatement.executeUpdate(Unknown Source)
        at com.mchange.v2.c3p0.impl.NewProxyPreparedStatement.executeUpdate(NewProxyPreparedStatement.java:105)
        at org.hibernate.id.insert.AbstractSelectingDelegate.performInsert(AbstractSelectingDelegate.java:57)
        ... 54 more'''

# input_stack_trace = '''Exception in thread "main" java.lang.NumberFormatException: For input string: "30k"
#             at java.lang.NumberFormatException.forInputString(NumberFormatException.java:65)
#             at java.lang.Integer.parseInt(Integer.java:580)
#             at java.lang.Integer.parseInt(Integer.java:615)
#             at NumberFormatExceptionTest.main(NumberFormatExceptionTest.java:3)'''

def get_links(input_stack_trace):
    if not check_for_java(input_stack_trace):
        print("Not a java stack trace")
        exit()

    exceptions = retrieve_exceptions(input_stack_trace)
    if len(exceptions) == 0:
        print("No exceptions found")
        exit()

    cause_exception = exceptions[-1]
    [exception_query, generic_query] = format_stackoverflow_query_string(cause_exception.exception, cause_exception.message)

    result = get_stackoverflow_links(exception_query, ["java"])

    if len(result['items']) < 5:
        non_tagged_results = get_stackoverflow_links(generic_query)
        result['items'].extend(non_tagged_results['items'])
        result['items'] = result['items'][0:5]

    top_results = []
    dump = {"results": top_results}
    for i in result['items']:
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
