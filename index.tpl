<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css" integrity="sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh" crossorigin="anonymous">
<title>代わりに読む人 Tweet Manager</title>
</head>
<body>
<div class="container">
<div class="row">
<div class="col-12 text-center">
    <h1>代わりに読む人</h1>
    <p>Tweet Manager v0.0</p>
</div>
<div class="col-12">
    <form class="form-inline justify-content-center" action="/" method="POST">
        <input class="form-control mx-1" type="text" name="username" placeholder="username">
        <input class="form-control mx-1" type="password" name="password" placeholder="password">
        <button type="submit" class="btn btn-primary my-2">Login</button>
    </form>
    <div>{{login}}</div>
</div>
</div>
</div>
% if login == True:
<script type="application/javascript">
    location.href="top.html"
</script>
% end
</body>
</html>