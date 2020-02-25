<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css" integrity="sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh" crossorigin="anonymous">
<title>Test</title>
</head>
<body>
<div class="container">
<div class="jumbotron jumbotron-fluid text-center" style="background-color: darkblue; color:#FFF;">
    <h1>代わりに読む人</h1>
    <p>Tweet Manager v0.0</p>
    <form class="form-inline justify-content-center" action="./top.html" method="get">
        <input type="date" name="from_date" class="form-control" value="2020-02-24" size="10">-<input type="date" class="form-control" name ="to_date" value="2020-02-27" size="10">
        &nbsp; <button class="btn btn-primary">View</button>
    </form>
</div>
<h2 class="text-primary">Tweet管理</h2>
<div class="row bg-white">
% import re, time, datetime
% for date in dates:
    <div class="col-sm-3 my-2 border-danger">
        <h4 class="text-secondary">{{date}}</h4>
      % for group in groups[date]:
        <div class="my-2">
            <h5 class="text-secondary">Tweet Group</h5>
            <div class="p-2 my-1 border outline-secondary  rounded tweet-group-settings d-none">
                <div class="mb-1">Start: <input type="time" class="form-control form-control-sm sched_start_time" value="{{datetime.datetime.strptime(group['sched_start_date'],'%Y-%m-%d %H:%M:%S').strftime('%H:%M:%S')}}" size="5"></div>
                <div class="my-1">Interval: <input type="integer" class="form-control form-control-sm" value="{{group['interval']}}" size="3"></div>
                <select class="form-control form-control-sm my-1"><option>{{group['status']}}</option><option>SCHEDULED</option></select>
                <div class="text-right"><button class="btn btn-sm btn-secondary small set-tweet-group">Set</button></div>
            </div>
            <div class="p-2 my-1 small border outline-secondary rounded tweet-group-settings-confirmed d-block">
                <div class="mb-1">Start: {{datetime.datetime.strptime(group['sched_start_date'],'%Y-%m-%d %H:%M:%S').strftime('%H:%M:%S')}}</div>
                <div class="my-1">Interval(sec): {{group['interval']}}</div>
                <div class="">Status: {{group['status']}}</div>
                <div class="text-right"><button class="btn btn-sm btn-secondary small edit-tweet-group">Edit</button></div>
            </div>
        % for tweet in tweets[group['gid']]:
            <div class="card my-1">
                <div class="card-header text-right small"><button class="btn btn-sm btn-outline-secondary save-tweet">Save</button> <button class="btn btn-sm btn-outline-secondary del-tweet">Delete</button></div>
                <div class="card-body">
                    <p class="card-text text-dark">{{tweet['text']}}</p>
                </div>
            </div>
        % end
            <div class="border outline-secondary rounded text-center text-secondary add-tweet">+</div>
        </div>
      % end
        <div class="border outline-secondary rounded text-center text-secondary my-2 add-tweet-group">Add Tweet Group</div>
    </div>
% end
</div>
<div class="row bg-white"><div class="col-12" style="height: 100px;"></div></div>
</div>
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>    
<script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js" integrity="sha384-Q6E9RHvbIyZFJoft+2mJbHaEWldlvI9IOYy5n3zV9zzTtmI3UksdQRVvoxMfooAo" crossorigin="anonymous"></script>
<script src="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.min.js" integrity="sha384-wfSDF2E50Y2D1uUdj0O3uMBJnjuUD4Ih7YwaYd1iqfktj0Uod8GCExl3Og8ifwB6" crossorigin="anonymous"></script>
<script>
    $(document).on('click', ".save-tweet", function(){
        alert($(this).parent().parent().find(".card-body").find(".card-text").html())
    })
    $(document).on('click', ".del-tweet", function(){
        $(this).parent().parent().remove()
    })
    $(document).on('click', ".edit-tweet-group", function(){
        /* 設定編集モードのトグル（開始） */
        $(this).parent().parent().parent().find(".tweet-group-settings-confirmed").addClass("d-none")
        $(this).parent().parent().parent().find(".tweet-group-settings-confirmed").removeClass("d-block")
        $(this).parent().parent().parent().find(".tweet-group-settings").addClass("d-block")
        $(this).parent().parent().parent().find(".tweet-group-settings").removeClass("d-none")
    })
    $(document).on('click', ".set-tweet-group", function(){


        /* 設定編集モードのトグル（終了） */
        $(this).parent().parent().parent().find(".tweet-group-settings").addClass("d-none")
        $(this).parent().parent().parent().find(".tweet-group-settings").removeClass("d-block")
        $(this).parent().parent().parent().find(".tweet-group-settings-confirmed").addClass("d-block")
        $(this).parent().parent().parent().find(".tweet-group-settings-confirmed").removeClass("d-none")

        /* 入力内容の取得 */
        alert($(this).parent().parent().find('.sched_start_time').val())
        time_l = $(this).parent().parent().find('.sched_start_time').val()
        // ★次回はここから！
        // status_l = 
        // interval_l = 

        /*
        /* 送信データの生成
        var send_vals = {}
        send_vals.gid = {{group['gid']}}
        send_vals.sched_start_date = time_l
        send_vals.status = status_l
        send_vals.interval = interval_l

        /* データ送信
        $.ajax({
          url:'api/1.0/update_tweet_group.json',
          type:'POST',
          contentType: 'application/JSON',
          data: JSON.stringify(send_vals),
          timeout: 10000,
          datatype: 'json'
        })
        .done(function(){
          pass
        })
        .fail(function(){
          alert("Failed.")
        })
        */
        
        
    })
    var card_template = '<div class="card my-2">' +
                '<div class="card-header text-right small"><button class="btn btn-sm btn-outline-secondary save-tweet">Save</button> <button class="btn btn-sm btn-outline-secondary del-tweet">Delete</button></div>' +
                '<div class="card-body">' +
                    '<p class="card-text text-dark"></p>' +
                '</div>' +
            '</div>'
    $(document).on('click', ".add-tweet", function(){
        $(this).before(card_template);
    })

    var tweet_group_template =
            '<div class="my-2">' +
                '<h5 class="text-secondary">Tweet Group</h5>' +
                '<div class="p-2 border outline-secondary  rounded tweet-group-settings d-none">' +
                    '<div class="mb-1">Start: <input type="time" class="form-control form-control-sm" value="20:00" size="5"></div>' +
                    '<div class="my-1">Interval: <input type="integer" class="form-control form-control-sm" value="60" size="3"></div>' +
                    '<select class="form-control form-control-sm my-1"><option>DRAFT</option><option>SCHEDULED</option></select>' +
                    '<div class="text-right"><button class="btn btn-sm btn-secondary small  set-tweet-group ">Set</button></div>' +
                '</div>' +
                '<div class="p-2 small border outline-secondary rounded tweet-group-settings-confirmed d-block">' +
                    '<div class="mb-1">Start: 20:00:00</div>' +
                    '<div class="my-1">Interval(sec): 60</div>' +
                    '<div class="">Status: SCHEDULED</div>' +
                    '<div class="text-right"><button class="btn btn-sm btn-secondary small edit-tweet-group">Edit</button></div>' +
                '</div>' +
                '<div class="border outline-secondary rounded text-center text-secondary add-tweet">+</div>' +
            '</div>'

    $(document).on('click', ".add-tweet-group", function(){
        $(this).before(tweet_group_template)
    })
</script>

</body>
</html>