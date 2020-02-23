<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="utf-8">
 <title>Test</title>
  <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css" integrity="sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh" crossorigin="anonymous">
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>    
  <script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js" integrity="sha384-Q6E9RHvbIyZFJoft+2mJbHaEWldlvI9IOYy5n3zV9zzTtmI3UksdQRVvoxMfooAo" crossorigin="anonymous"></script>
  <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.min.js" integrity="sha384-wfSDF2E50Y2D1uUdj0O3uMBJnjuUD4Ih7YwaYd1iqfktj0Uod8GCExl3Og8ifwB6" crossorigin="anonymous"></script>
</head>
<body>
<style>
    body {
        background-color: #f9f9f9;
        margin: 0px 0px 0px 0px;
        padding: 0px 0px 0px 0px;
    }

    header { text-align: center; background-color: #e0e0e0}
    article { background-color: #e0e0e0}
    .tweet-group-settings { display: none }
    .tweet-group-settings-confirmed { display: inline }    
    .date-container {
        margin: 0px auto 5px auto;
        padding: 0px 0px 0px 0px;
        max-width: 100%;
        background-color: #f0f0f0;
    }
    .tweet-group-container { background-color: whitesmoke; padding: 4px; margin: 4px}
    .tweet { padding: 0px; margin: 2px; background-color: #fafafa}
    .tweet-text { padding: 2px;}
    .tweet-footer { text-align: right; font-size: 0.5em; color: gray;}

  % for date in dates:
  % for group in groups[date]:
    #tweet-group-settings-form-{{group['gid']}} {
        display: none;
    }
    #tweet-group-settings-form-{{group['gid']}}-confirmed {
        display: inline;
    }
  % end
  % end

</style>
<div class="container">
<header>
  <h1>代わりに読む人 Scheduled Tweets 管理画面</h1>
  <form action="./top.html" method="get">
    <p>表示期間 <input type="date" name="from_date" value="{{dates[0]}}">~<input type="date" name="to_date" value="{{dates[-1]}}"> <input type="submit"></p>
  </form>
</header>
<article>
</article>
<article>
    % for date in dates:
    <div class="date-container" id="date-{{date}}">
    <h2>{{date}}</h2>
      % for group in groups[date]:
      <div class="tweet-group-container" id="tweet-group-{{group['gid']}}">
        <span id="tweet-group-settings-form-{{group['gid']}}"> 開始時刻<input type="time" name="time" value="{{group['sched_start_date']}}"> 状態 <select name="status" value="{{group['status']}}"><option>DRAFT</option><option>SCHEDULED</option></select> <button id="tweet-group-settings-form-{{group['gid']}}-btn">確定</button></span>
        <span id="tweet-group-settings-form-{{group['gid']}}-confirmed">開始時刻 <span id="tweet-group-settings-form-{{group['gid']}}-confirmed-time">{{group['sched_start_date']}}</span>
            状態 <span id="tweet-group-settings-form-{{group['gid']}}-confirmed-status">{{group['status']}}</span></span> <span id="btn-edit-tweet-group-{{group['gid']}}">[Edit]</span>[Remove]
        % for tweet in tweets[group['gid']]:
          <div class="tweet" id="tweet-{{tweet['id']}}">
          <div class="tweet-footer">{{tweet['subid']}}: {{tweet['status']}} [Edit][Remove]</div>
          <div class="tweet-text" contenteditable="True">{{tweet['text']}}</div>
          </div>
        % end
          <p id="add-tweet-btn-{{group['gid']}}">ツイートを追加する [+]</p>
      </div>
      % end
        <p id="add-tweet-group-btn-{{date}}">グループを追加する [+]</p>  
    </div>
    % end
</article>
<script>
  % for date in dates:
    $("#add-tweet-group-btn-{{date}}").click(function(){
      var gid_new = 0; var sched_start_date_new = '1978-10-03 00:00:00'; var status_new = 'DRAFT';
      var tweet_group_new = '<div class="tweet-group-container" id="tweet-group-' + gid_new + '"> <span id="tweet-group-settings-form-' + gid_new +'"> 開始時刻 <input type="time" name="time" value="' + sched_start_date_new + '"> 状態 <select name="status" value="' + status_new + '"><option>DRAFT</option><option>SCHEDULED</option></select> <button id="tweet-group-settings-form-' + gid_new + '-btn">確定</button></span> <span id="tweet-group-settings-form-' + gid_new + '-confirmed">開始時刻 <span id="tweet-group-settings-form-' + gid_new + '-confirmed-time">' + sched_start_date_new +'</span> 状態 <span id="tweet-group-settings-form-' + gid_new + '-confirmed-status">' +status_new+ '</span></span> <span id="btn-edit-tweet-group-' +gid_new+ '">[Edit]</span>[Remove]</div>'
      $("#add-tweet-group-btn-{{date}}").prepend(tweet_group_new)


    })
    % for group in groups[date]:
      $("#btn-edit-tweet-group-{{group['gid']}}").click(
        function(){
          $("#tweet-group-settings-form-{{group['gid']}}").css("display", "inline");
          $("#tweet-group-settings-form-{{group['gid']}}-confirmed").css("display", "none");
        })
      $("#tweet-group-settings-form-{{group['gid']}}-btn").click(
        function(){
          time_l = $('#tweet-group-settings-form-{{group['gid']}} [name=time]').val()
          status_l = $('#tweet-group-settings-form-{{group['gid']}} [name=status]').val()
          $("#tweet-group-settings-form-{{group['gid']}}-confirmed-time").html(time_l)
          $("#tweet-group-settings-form-{{group['gid']}}-confirmed-status").html(status_l)
          $("#tweet-group-settings-form-{{group['gid']}}").css("display", "none");
          $("#tweet-group-settings-form-{{group['gid']}}-confirmed").css("display", "inline");
          var send_vals = {}
          send_vals.gid = {{group['gid']}}
          send_vals.sched_start_date = time_l
          send_vals.status = status_l
          $.ajax({
              url:'api/1.0/update_tweet_group.json',
              type:'POST',
              contentType: 'application/JSON',
              data: JSON.stringify(send_vals),
              timeout: 10000,
              datatype: 'json'
          })
          .done(function(){
              alert("done")
          })
        }
      )
      $("#add-tweet-btn-{{group['gid']}}").click(function(){
        $("#add-tweet-btn-{{group['gid']}}").before('<div class="tweet"><p class="tweet-text" contenteditable="True"></p><p><span class="tweet-footer">: [Edit][Remove]</span></p></div>');
      })

      % for tweet in tweets[group['gid']]:
        $("#tweet-{{tweet['id']}}").click(
          function(){
            $("#tweet-3").find(".tweet-text").css("contenteditable", "False")
          }
        )
      % end
    % end
  % end
</script>
</div>
</body>
</html>