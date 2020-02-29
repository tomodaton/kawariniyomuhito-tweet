<html>
<head>
 <title>代わりに読む人 Tweet Manager</title>
  <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css" integrity="sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh" crossorigin="anonymous">
</head>
<body>
    {{name}}

    <p>
        <span id="test1">List of groups</span> <span id="test2">test2</span>
    </p>
    <p>
        <span id="read1">read1</span> <span id="read2">read2</span>
    </p>
    
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>    
    <script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js" integrity="sha384-Q6E9RHvbIyZFJoft+2mJbHaEWldlvI9IOYy5n3zV9zzTtmI3UksdQRVvoxMfooAo" crossorigin="anonymous"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.min.js" integrity="sha384-wfSDF2E50Y2D1uUdj0O3uMBJnjuUD4Ih7YwaYd1iqfktj0Uod8GCExl3Og8ifwB6" crossorigin="anonymous"></script>
    
    <script>
        $(function(){
            $("#read1").click(function(){
                $("#read1").css("color", "red")
                $.ajax({
                    type: 'GET',
                    url: 'http://localhost:8081/test1.html',
                    datatype: 'html',
                    timeout: 100
                })
                .done(function(data){
                    $("#read1").html(data)
                })
                .fail(function(data){
                    alert("Failed")
                })
            })
        });
    </script>
    
</body>
</html>