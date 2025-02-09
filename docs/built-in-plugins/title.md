# Title
The title plugin simply searches for the text `%title%` and replaces it with the name of the file without the file
extension. As an example, below is the default HTML template used by PyMind:

```HTML
<!DOCTYPE html>
<!-- MARKER -->
<html>
<head>
    <title>%title%</title>
    <link href="%css%" rel="stylesheet">
</head>
<body>
%nav%
<div class="content">
%content%
</div>
{{footer}}
</body>
</html>
```
