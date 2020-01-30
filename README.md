# why_connector
Data-Mediation between applications - Early work in progress

The **why_connector** is an application used for data mediation between applications. It is our newest open-source project, thus is in an very early stage of planing, testing, desining and simply playing around. 

Currently, the **why_connector** is able to listen for incoming requests on a hosting werbserver and processes them. Requests are processes by forming a t-SQL Query based on the request itself, following the REST schema. The resulting t-SQL Query is executed against a specified host and the resulting data gets returned in JSON-Format.
