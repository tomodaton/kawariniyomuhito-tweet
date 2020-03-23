<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css" integrity="sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh" crossorigin="anonymous">
<script src="https://kit.fontawesome.com/89affe3549.js" crossorigin="anonymous"></script>
<title>代わりに読む人 Tweet Manager</title>
</head>
<body>
<div class="container">
<div class="jumbotron jumbotron-fluid text-center px-4" style="background-color: darkblue; color:#FFF;">
    <h1>代わりに読む人</h1>
    <p>Tweet Manager v0.0</p>
    <form class="form-inline justify-content-center" action="./top.html" method="get">
        <input type="date" name="from_date" class="form-control" value="{{dates[0]}}" size="10">-<input type="date" class="form-control" name ="to_date" value="{{dates[-1]}}" size="10">
        &nbsp; <button class="btn btn-primary my-2">View</button>
    </form>
</div>
<div class="row bg-white">
% import re, time, datetime
% for date in dates:
    <div class="col-sm-3 my-2 border-danger">
        <h4 class="date text-secondary">{{date}}</h4>
      % for group in groups[date]:
        <div class="my-2">
            <h5 class="text-secondary">Tweet Group</h5>
            <div class="p-2 my-1 border outline-secondary  rounded tweet-group-settings d-none shadow-sm">
                <div class="text-right"><button class="btn btn-sm btn-secondary small set-tweet-group">Set</button></div>
                <div class="tweet-group-setting-gid d-none">{{group['gid']}}</div>
                <div class="mb-1">Start: <input type="time" class="form-control form-control-sm sched-start-time" value="{{datetime.datetime.strptime(group['sched_start_date'],'%Y-%m-%d %H:%M:%S').strftime('%H:%M:%S')}}" size="8"></div>
                <div class="my-1">Interval: <input type="integer" class="form-control form-control-sm tweet-group-interval" value="{{group['interval']}}" size="3"></div>
                <select class="form-control form-control-sm my-1 tweet-group-status"><option>DRAFT</option><option>SCHEDULED</option></select>
            </div>
            <div class="p-2 my-1 small border outline-secondary rounded tweet-group-settings-confirmed d-block shadow-sm">
                <div class="text-right"><button class="btn btn-sm btn-outline-secondary small edit-tweet-group">Edit</button> <button class="btn btn-sm btn-outline-secondary small delete-tweet-group">Del</button></div>
                <div class="tweet-group-setting-gid d-none">{{group['gid']}}</div>
                <div class="mb-1">Start: <span class="sched-start-time">{{datetime.datetime.strptime(group['sched_start_date'],'%Y-%m-%d %H:%M:%S').strftime('%H:%M:%S')}}</span></div>
                <div class="my-1">Interval(sec): <span class="tweet-group-interval">{{group['interval']}}</span></div>
                <div class="">Status: <span class="tweet-group-status">{{group['status']}}</span></div>
            </div>
        % for tweet in tweets[group['gid']]:
            <div class="card my-1 shadow-sm">
                <div class="tweet-id d-none">{{tweet['id']}}</div>
                <div class="tweet-subid d-none">{{tweet['subid']}}</div>
                <div class="rt-flag d-none">{{tweet['rt_flag']}}</div>
                <div class="card-header text-right">
                    <div class="row">
                        <div class="px-2 text-left">
                            % if tweet['rt_flag'] == 0:
                            <i class="fas fa-edit" style="color: #60a0ff"></i> 
                            <i class="fas fa-retweet text-secondary"></i>
                            % else:
                            <i class="fas fa-edit text-secondary"></i> 
                            <i class="fas fa-retweet" style="color: #60a0ff"></i>
                            % end
                        </div>
                        <div class="px-2 ml-auto">
                            <i class="far fa-trash-alt text-secondary del-tweet"></i>
                        </div>
                    </div>
                </div>
                <div class="card-body">
                    % if tweet['rt_flag'] == 0:
                    <textarea class="card-text text-dark tweet-text" style="border: 0px; width: 100%">{{tweet['text']}}</textarea>
                    <textarea class="card-text text-dark org-tweet-id d-none" style="border: 0px; width: 100%">{{tweet['org_tweet_id']}}</textarea>
                    <textarea class="card-text text-dark org-tweet-text d-none" style="border: 0px; width: 100%"></textarea>
                    <p class="card-text text-dark org-tweet-text d-none" style="border: 0px; width: 100%">{{tweet['org_tweet_text']}}</p>
                    % else:
                    <textarea class="card-text text-dark tweet-text d-none" style="border: 0px; width: 100%">{{tweet['text']}}</textarea>
                    <textarea class="card-text text-dark org-tweet-id" style="border: 0px; width: 100%">{{tweet['org_tweet_id']}}</textarea>
                    <p class="card-text text-dark org-tweet-text d-none" style="border: 0px; width: 100%">{{tweet['org_tweet_text']}}</p>
                    % end
                    <div class="text-right">
                        <i class="fas fa-arrow-circle-up text-secondary save-tweet"></i>
                    </div>
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
<script src="scripts/apioperations.js"></script>
</body>
</html>
