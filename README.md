# HTTP-Program

Python server-client program that implements a simplified HTTP Protocol

HTTP Client uses TCP sockets to perform the following:  
Reads in a single command line input that specifies web url, hostname, server port, and name of file to be fetched (localhost:12000/filename.html for example).  
If the file is not cached in the system, use a HTTP GET request to fetch file named via URL and print contents of file then cache file with HTTP/1.1 200 OK code. 
If the file is cached, use a Condition GET request for the file named in the URL, if the server indicates the file has not been modified since last request print HTTP/1.1 304 Not Modified code. Otherwise indicate file modification, cache and print new content with new last modified date.

HTTP Server uses TCP sockets to perform the following:  
Reads in IP address and Server port via command line args. 
Open a TCP socket and loop for incoming HTTP GET or Condition GET requests from one or more HTTP clients. 
Respond appropriately to GET or Conditional GET requests using 200 OK, 304 Not Modified, or 404 Not Found.
