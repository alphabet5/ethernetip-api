# ethernetip-api

This is a simple api to read/write tags using pycomm3 library. 

The excel file uses the following for an easy setup of the api requests and json constructing and parsing.
- VBA-tools/VBA-Web
- VBA-tools/VBA-JSON
- VBA-tools/VBA-Dictionary (Included with VBA-tools/VBA-Web)

## Requirements

- python3 (tested with 3.9)
- pycomm3
- flask

## Usage

The example Excel file contains a simple example of reading and writing tags.

- Install the dependencies including python3.
- Run the python file to start the web server. (by default runs at http://127.0.0.1:5000)

Reading:
```bash
curl 127.0.0.1:5000/?plc=ip_address/backplane/slot&tag=Tag_Name
```
Writing:
```bash
curl --location --request PUT '127.0.0.1:5000/?plc=ip_address/backplane/slot&tag=Tag_Name&value=0'
```


Within VBA:
```vba
Public Function ReadTag(plc As String, tag As String)
    Dim client As New WebClient
    client.BaseUrl = "http://127.0.0.1:5000/"
    Dim Resource As String
    Dim Response As WebResponse
    Resource = "?plc=" & plc & "&tag=" & tag
    Set Response = client.GetJson(Resource)
    ReadTag = Response.Data("val")
End Function

Public Function WriteTag(plc As String, tag As String, value As Variant)
    Dim client As New WebClient
    client.BaseUrl = "http://127.0.0.1:5000/"
    Dim put_obj As New WebRequest
    put_obj.Method = HttpPut
    put_obj.AddQuerystringParam "plc", plc
    put_obj.AddQuerystringParam "tag", tag
    put_obj.AddQuerystringParam "value", value
    Dim Response As WebResponse
    Set Response = client.Execute(put_obj)
    WriteTag = Response.StatusCode
End Function
```



## Future

- Better support for arrays.
- Sending multiple read/write requests over a single api call.
- Tests.
- Error handling.
- Optimization.
