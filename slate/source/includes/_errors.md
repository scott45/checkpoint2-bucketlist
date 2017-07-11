# Errors

<aside class="notice">This error section is stored in a separate file in `includes/_errors.md`. Slate allows you to optionally separate out your docs into many files...just save them to the `includes` folder and add them to the top of your `index.md`'s frontmatter. Files are included in the order listed.</aside>

The Bucketlist API uses the following error codes:


Error Code | Meaning
---------- | -------
400 | Bad Request -- Your request truly sucks
200 | Ok
201 | Ok resulting in the creation of something e.g Registration
401 | Unauthorized -- Your API key is wrong
403 | Forbidden -- The bucket requested is hidden for administrators only
404 | Not Found -- The specified request could not be found
405 | Method Not Allowed -- You tried to access a bucket with an invalid method
406 | Not Acceptable -- You requested a format that isn't json
410 | No longer here -- The bucket requested has been removed from our servers
429 | Too Many Requests -- You're requesting too many buckets! Relax your requests
500 | Internal Server Error -- We had a problem with our server. Try again later.
503 | Service Unavailable -- We're temporarily offline for maintenance. Please try again later.
