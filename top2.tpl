<html>
<head>
 <title>Test</title>
  <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css" integrity="sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh" crossorigin="anonymous">
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>    
  <script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js" integrity="sha384-Q6E9RHvbIyZFJoft+2mJbHaEWldlvI9IOYy5n3zV9zzTtmI3UksdQRVvoxMfooAo" crossorigin="anonymous"></script>
  <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.min.js" integrity="sha384-wfSDF2E50Y2D1uUdj0O3uMBJnjuUD4Ih7YwaYd1iqfktj0Uod8GCExl3Og8ifwB6" crossorigin="anonymous"></script>
</head>
<body>
<style>
    h1 { font-size: 1.5em; }
    h2 { font-size: 1.4em; }
    p { font-size: 1.0em; }
    .tweet-group-settings { display: none };
    .tweet-group-settings-confirmed { display: inline };
</style>
<header>
  <h1>代わりに読む人 Scheduled Tweets 管理画面</h1>
  <p>表示期間 <input type="date" name="fromdate" value="2020-02-22">~<input type="date" name="todate" value="2020-02-28"></p>
</header>
<article>
<div class="date-container">
    <h2>2020-02-22</h2>
    <span>グループ追加</span>
    <div class="tweet-group">
        <div class="tweet-group-settings-confirmed">開始時刻 <span class="tweet-group-settings-confirmed-time">00:00</span> 間隔(秒) 60 状態 SCHEDULED</div>
        <div class="tweet-group-settings">
            開始時刻 <input type="time" name="" value="20:00">
            間隔(秒) <input type="number" name="" value="60" min="1" max="300">
            状態 <select name="status">
                <option value="SCHEDULED">SCHEDULED</option>
                <option value="SCHEDULED">DRAFT</option>
                <option value="SCHEDULED">SUCCESS</option></select>
                <button class="tweet-group-settings-submit" >確定</button>
        </div>
        <p>aa</p>
    </div>
</div>
<script>
    $(".tweet-group-settings-confirmed").click(function(){
        $(".tweet-group-settings-confirmed").css("display", "none");
        $(".tweet-group-settings").css("display", "inline");
    });
    $(".tweet-group-settings-submit").click(function(){
        /* 入力値の取得 */
        alert($('time').html())
        /* var var_time = $('[name=status]').html(); */
        /* 取得した値のセット */
        alert(var_time)
        $('.tweet-group-settings-confirmed-time').html(var_time);
        $(".tweet-group-settings-confirmed").css("display", "inline");
        $(".tweet-group-settings").css("display", "none");
    });
</script>
<div class="date-container">
  <h2>2020-02-23</h2>
  <span>グループ追加</span>
</div>
<div class="date-container">
  <h2>2020-02-24</h2>
  <span>グループ追加</span>
</div>
<div class="date-container">
  <h2>2020-02-25</h2>
  <span>グループ追加</span>
</div>
<div class="date-container">
  <h2>2020-02-26</h2>
  <span>グループ追加</span>
</div>
<div class="date-container">
  <h2>2020-02-27</h2>
  <span>グループ追加</span>
</div>
    <div class="date-container">
  <h2>2020-02-28</h2>
  <span>グループ追加</span>
</div>
</article>   
</body>
</html>