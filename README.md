# jscom-notion-qr-service

A serverless service that uses the notion api to create and add QR codes to notion pages. This receives a webhook from 
Notion for a given trigger and proceeds to create a QR code for the originating page, adding it to a property/column 
specified in a webhook header.

## Architecture

A webhook is received through api-gateway, which triggers a lambda function that generates a QR code and copies it to
S3.

The lambda function then updates the Notion page with the QR code URL hosted in S3.

## Configuring Notion

1. Create a new `internal` integration in Notion, save the key for later.
2. Share the page you want to add QR codes to with the integration.
3. Create a new webhook for the page you want to add QR codes to, using the api-gateway endpoint as the target (e.g. `https://api.johnsosoka.com/v1/notion/qr`).
4. Add a header to the webhook with your notion integration key from step 1 as the value for field `x-notion-token`.
5. Add a header to the webhook with a field name of `x-column-name` with a value of the column name you want to add the QR code to.

I'm aware that I probably shouldn't have prefixed the custom headers with `x`, I wrote this over a long vacation and didn't 
think about it until after I had already deployed it. I'll fix it in a future version.


## History

* This project is a deployable version of [this](https://gist.github.com/johnsosoka/1ce8b0ac81cec27fb447093a1a99f196) gist.
* My Notion/QR code journey started in this [blog post](https://www.johnsosoka.com/note/2023/12/28/qr-code-box-organization.html).