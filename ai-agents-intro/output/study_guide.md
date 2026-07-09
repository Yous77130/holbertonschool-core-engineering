# Topic: HTTP Status Codes

## Simple Explanation

When you visit a website or send a request to a server, the server responds with a message indicating whether the request was successful or not. This message is called an HTTP (Hypertext Transfer Protocol) response. The response includes a status code, which is a three-digit number that indicates the outcome of the request.

Think of HTTP status codes like report cards for your requests to the server. Each code tells you what happened with your request and whether it was successful or not.

## Key Concepts

* **Success codes**: 1xx-2xx (informational), 200-299 (OK)
	+ These codes indicate that the request was successfully processed.
* **Redirection codes**: 300-399
	+ These codes tell you to go somewhere else, like a different page or website.
* **Client error codes**: 400-499
	+ These codes mean there's something wrong with your request, like incorrect data or unauthorized access.
* **Server error codes**: 500-599
	+ These codes indicate that the server had a problem processing your request.

## Example

Let's say you enter your login credentials to access a website. The server responds with an HTTP status code:

**200 OK**: Your login was successful, and you're now logged in!

But if you enter incorrect login credentials...

**403 Forbidden**: Oops, it looks like those aren't the right credentials! You'll need to try again.

If the server is having trouble processing your request...

**503 Service Unavailable**: Sorry, our server is down for maintenance. Try again later!