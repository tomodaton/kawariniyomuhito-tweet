function toggle_navbar_to_home_timeline(){
        $('.scheduled-tweet').addClass('d-none')
        $('.scheduled-tweet').removeClass('d-block')
        $('.to-scheduled-tweet').removeClass('active')
        $('.help').addClass('d-none')
        $('.help').removeClass('d-block')
        $('.to-help').removeClass('active')

        $('.home-timeline').addClass('d-block')
        $('.home-timeline').removeClass('d-none')
        $('.to-home-timeline').addClass('active')
}
function toggle_navbar_to_scheduled_tweet(){
        $('.home-timeline').addClass('d-none')
        $('.home-timeline').removeClass('d-block')
        $('.to-home-timeline').removeClass('active')
        $('.help').addClass('d-none')
        $('.help').removeClass('d-block')
        $('.to-help').removeClass('active')

        $('.scheduled-tweet').addClass('d-block')
        $('.scheduled-tweet').removeClass('d-none')
        $('.to-scheduled-tweet').addClass('active')
}       
function toggle_navbar_to_help(){
        $('.home-timeline').addClass('d-none')
        $('.home-timeline').removeClass('d-block')
        $('.to-home-timeline').removeClass('active')
        $('.scheduled-tweet').addClass('d-none')
        $('.scheduled-tweet').removeClass('d-block')
        $('.to-scheduled-tweet').removeClass('active')

        $('.help').addClass('d-block')
        $('.help').removeClass('d-none')
        $('.to-help').addClass('active')

}       

$(document).on('click', ".save-tweet", function(){
    // alert($(this).parent().parent().find(".card-body").find(".card-text").html())
    // $(this).parent().parent().find(".card-body").find(".card-text").removeAttr('contenteditable')
    
    /* Tweet/Retweet判定 */
    rt_flag = $(this).parent().parent().parent().find('.rt-flag').html()
    if ( rt_flag == 0 ) {
        alert("Tweet")
    } else {
        alert("Retweet")
    }
    
    if ( rt_flag == 0 ) {
        /* データ作成 */
        // send: text, gid, subid
        var send_vals = {}
        send_vals.id = $(this).parent().parent().parent().find('.tweet-id').html()
        // alert(send_vals.id)
        send_vals.rt_flag = 0
        send_text = $(this).parent().parent().find(".tweet-text").val().replace(/<.*?>/g, '')
        send_vals.text = send_text
        $(this).parent().parent().parent().find(".tweet-text").val(send_text)
        // send_vals.text = $(this).parent().parent().find(".card-body").find(".card-text").html() // receive: id // alert(send_vals.gid); 
        _this = $(this)
        /* データ送信 */
        $.ajax({
          url: '/api/1.0/update_tweet.json',
          type: 'POST',
          contentType: 'application/JSON',
          data: JSON.stringify(send_vals),
          timeout: 10000,
          datatype: 'json'
        })
        .done(function(data){
            // alert(data['id']);
            _this.removeClass("text-danger")
            _this.addClass("text-secondary")

        })
        .fail(function(){
            _this.removeClass("text-secondary")
            _this.addClass("text-danger")
            alert("Failed.")
        })
    } else {
        /* データ作成 */
        // send: org_tweet_id, gid, subid
        var send_vals = {}
        send_vals.id = $(this).parent().parent().parent().find('.tweet-id').html()
        send_vals.rt_flag = 1
        send_vals.org_tweet_id = $(this).parent().parent().find(".org-tweet-id").val().replace(/^http.*\/([0-9]*).*/,'$1').replace(/([0-9]*).*/, '$1')
        alert(send_vals.org_tweet_id)
        $(this).parent().parent().find(".org-tweet-id").val(send_vals.org_tweet_id)
        // send_vals.text = $(this).parent().parent().find(".card-body").find(".card-text").html()
        // alert(send_vals.gid); 
        _this = $(this)
        /* データ送信 */
        $.ajax({
          url: '/api/1.0/update_tweet.json',
          type: 'POST',
          contentType: 'application/JSON',
          data: JSON.stringify(send_vals),
          timeout: 10000,
          datatype: 'json'
        })
        .done(function(data){
            _this.removeClass("text-danger")
            _this.addClass("text-secondary")
            _this.parent().parent().find('.org-tweet-text').removeClass('d-none')
            _this.parent().parent().find('.org-tweet-text').addClass('d-block')
            _this.parent().parent().find('.org-tweet-text').html(data['org_tweet_text'])
            _this.parent().parent().find('.org-tweet-id').removeClass('d-block')
            _this.parent().parent().find('.org-tweet-id').addClass('d-none')
        })
        .fail(function(){
            _this.removeClass("text-secondary")
            _this.addClass("text-danger")
            alert("Failed.")
        })
    }  
})

$(document).on({
    'mouseenter': function(){
        $(this).removeClass("text-secondary");
        $(this).addClass("text-active")
    },
    'mouseleave': function(){
        $(this).removeClass("text-active");
        $(this).addClass("text-secondary")
    }
}, ".save-tweet")

$(document).on('click', ".del-tweet", function(){
    
    /* データ作成 */
    // send: text, gid, subid
    var send_vals = {}
    send_vals.id = $(this).parent().parent().parent().parent().find('.tweet-id').html()
    // alert(send_vals.id)
    
    _this = $(this)
    /* データ送信 */
    $.ajax({
      url: '/api/1.0/delete_tweet.json',
      type: 'POST',
      contentType: 'application/JSON',
      data: JSON.stringify(send_vals),
      timeout: 10000,
      datatype: 'json'
    })
    .done(function(data){
        // alert(data['id']);
        _this.parent().parent().parent().parent().remove()
    })
    .fail(function(){
        alert("Failed.")
    })
})

$(document).on({
    'mouseenter': function(){
        $(this).removeClass("text-secondary");
        $(this).addClass("text-active")
    },
    'mouseleave': function(){
        $(this).removeClass("text-danger");
        $(this).addClass("text-secondary")
    }
}, ".del-tweet")

$(document).on({
    'mouseenter': function(){
        $(this).addClass("text-primary")
    },
    'mouseleave': function(){
        $(this).removeClass("text-primary");
    }
}, ".fa-edit")

$(document).on({
    'mouseenter': function(){
        $(this).addClass("text-primary")
    },
    'mouseleave': function(){
        $(this).removeClass("text-primary");
    }
}, ".fa-retweet")

$(document).on('click', ".fa-edit", function(){
    $(this).parent().parent().parent().parent().find(".rt-flag").html("0")

    /* Tweet text と RTするTweetの org-tweet-idの表示をトグル */
    $(this).parent().parent().parent().parent().find(".tweet-text").addClass("d-block")
    $(this).parent().parent().parent().parent().find(".tweet-text").removeClass("d-none")
    $(this).parent().parent().parent().parent().find(".org-tweet-id").addClass("d-none")
    $(this).parent().parent().parent().parent().find(".org-tweet-id").removeClass("d-block")
    $(this).parent().parent().parent().parent().find(".org-tweet-text").addClass("d-none")
    $(this).parent().parent().parent().parent().find(".org-tweet-text").removeClass("d-block")

    /* Tweet(edit)ボタンとRetweetボタンのトグル */
    $(this).parent().find(".fa-retweet").removeClass("text-primary")
    $(this).parent().find(".fa-retweet").addClass("text-secondary")
    $(this).parent().find(".fa-retweet").css("color", "");
    $(this).removeClass("text-secondary");
    $(this).css("color", "#60a0ff")
})

$(document).on('click', ".fa-retweet", function(){
    $(this).parent().parent().parent().parent().find(".rt-flag").html("1")

    /* Tweet text と RTするTweetの org-tweet-idの表示をトグル */
    $(this).parent().parent().parent().parent().find(".org-tweet-id").addClass("d-block")
    $(this).parent().parent().parent().parent().find(".org-tweet-id").removeClass("d-none")
    $(this).parent().parent().parent().parent().find(".tweet-text").addClass("d-none")
    $(this).parent().parent().parent().parent().find(".tweet-text").removeClass("d-block")
    // $(this).parent().parent().parent().parent().find(".org-tweet-text").addClass("d-block")
    // $(this).parent().parent().parent().parent().find(".org-tweet-text").removeClass("d-none")

    /* Tweet(edit)ボタンとRetweetボタンのトグル */
    $(this).parent().find(".fa-edit").removeClass("text-primary")
    $(this).parent().find(".fa-edit").addClass("text-secondary")
    $(this).parent().find(".fa-edit").css("color", "");
    $(this).removeClass("text-secondary");
    $(this).css("color", "#60a0ff")
})

$(".tweet-text").autosize()

$(".tweet-text").each(function(){
    var cnt = $(this).val().length;
    $(this).parent().find(".cnt-text").text(cnt)
})

$(document).on('keydown keyup click', ".tweet-text", function(){
    var cnt = $(this).val().length;
    $(this).parent().find(".cnt-text").text(cnt)
})


$(document).on('click', ".org-tweet-text", function(){
    $(this).parent().find(".org-tweet-id").removeClass("d-none")
    $(this).parent().find(".org-tweet-id").addClass("d-block")
    $(this).removeClass("d-block")
    $(this).addClass("d-none")
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
    date_l = $(this).parent().parent().parent().parent().find('.date').html() 
    gid_l = $(this).parent().parent().find('.tweet-group-setting-gid').html()
    time_l = $(this).parent().parent().find('.sched-start-time').val()
    status_l = $(this).parent().parent().find('.tweet-group-status').val()
    interval_l = $(this).parent().parent().find('.tweet-group-interval').val()

    /* 入力内容のチェック (time_l) */
    /* フォーマット1(HH:mm:ss)はOK、フォーマット2(HH:mm)はHH:mm:00に、それ以外は"00:00:00"に変換 */
    var time_pattern = /^[0-9]{2}:[0-9]{2}:[0-9]{2}$/
    var time_pattern2 = /^[0-9]{2}:[0-9]{2}$/
    if (time_l.match(time_pattern) == null ) {
        if (time_l.match(time_pattern2) == null ) {
            time_l = '00:00:00'
        } else {
            time_l = time_l + ':00'
        }
    }

    /* 入力内容のチェック (interval) */
    var interval_pattern = /^[1-9][0-9]{0,2}$/
    if (interval_l.match(interval_pattern) == null) {
        interval_l = 60
    }

    datetime_l = date_l + ' ' + time_l    
    $(this).parent().parent().parent().find('.tweet-group-settings-confirmed').find('.tweet-group-setting-gid').html(gid_l)
    $(this).parent().parent().parent().find('.tweet-group-settings-confirmed').find('.sched-start-time').html(time_l)
    $(this).parent().parent().parent().find('.tweet-group-settings-confirmed').find('.tweet-group-status').html(status_l)
    $(this).parent().parent().parent().find('.tweet-group-settings-confirmed').find('.tweet-group-interval').html(interval_l)

    /* 送信データの生成 */
    var send_vals = {}
    send_vals.gid = gid_l
    send_vals.sched_start_date = datetime_l
    send_vals.status = status_l
    send_vals.interval = interval_l

    /* データ送信 */
    $.ajax({
      url:'api/1.0/update_tweet_group.json',
      type:'POST',
      contentType: 'application/JSON',
      data: JSON.stringify(send_vals),
      timeout: 10000,
      datatype: 'json'
    })
    .done(function(){
        ;
    })
    .fail(function(){
        alert("Failed.")
    })    
})


$(document).on('click', ".delete-tweet-group", function(){

    /* データ送信 */
    var send_vals = {}
    gid_l = $(this).parent().parent().parent().find('.tweet-group-setting-gid').html()
    send_vals.gid = gid_l

    alert(gid_l)
    _this =$(this)

    $.ajax({
      url:'api/1.0/delete_tweet_group.json',
      type:'POST',
      contentType: 'application/JSON',
      data: JSON.stringify(send_vals),
      timeout: 10000,
      datatype: 'json'
    })
    .done(function(data){
        _this.parent().parent().parent().remove()
    })
    .fail(function(){
        alert("Failed.")
    })
})


var card_template = '<div class="card my-1 shadow-sm">' +
                '<div class="tweet-id d-none"></div>' +
                '<div class="tweet-subid d-none"></div>' +
                '<div class="rt-flag d-none">0</div>' +
                '<div class="card-header text-right">' +
                    '<div class="row">' +
                        '<div class="px-2 text-left">' +
                            '<i class="fas fa-edit" style="color: #60a0ff"></i> ' +
                            '<i class="fas fa-retweet text-secondary"></i>' +
                        '</div>' +
                        '<div class="px-2 ml-auto">' +
                            '<i class="far fa-trash-alt text-secondary del-tweet"></i>' +
                        '</div>' +
                    '</div>' +
                '</div>' +
                '<div class="card-body">' +
                    '<textarea class="card-text text-dark tweet-text" placeholder="Input Your Tweet" style="border: 0px; width: 100%"></textarea>' +
                    '<textarea class="card-text text-dark org-tweet-id d-none"  placeholder="Input Link to tweet" style="border: 0px; width: 100%"></textarea>' +
                    '<p class="card-text text-dark org-tweet-text d-none small border rounded p-1 bg-light" style="border: 0px; width: 100%"></p>' +
                    '<div class="text-right">' +
                        '<i class="fas fa-arrow-circle-up text-secondary save-tweet"></i>' +
                    '</div>' +
                '</div>' +
            '</div>'

$(document).on('click', ".add-tweet", function(){

    $(this).before(card_template);
    prev_subid = $(this).prev().prev().find(".tweet-subid").html()
    // alert(prev_subid)
    if ( prev_subid == ''  | prev_subid == null ){
        prev_subid = 1
    } else {
        prev_subid = parseInt(prev_subid,10)+1
    }
    $(this).prev().find(".tweet-subid").html(prev_subid)
    // alert(prev_subid)
    /* データ作成 */
    // send: text, gid, subid
    var send_vals = {}
    send_vals.rt_flag = $(this).prev().find(".rt-flag").html()
    send_vals.gid = $(this).parent().find('.tweet-group-setting-gid').html()
    send_vals.subid = $(this).prev().find(".tweet-subid").html()
    send_vals.text = ''
    // receive: id
    // alert(send_vals.gid);
    
    _this = $(this)
    /* データ送信 */
    $.ajax({
      url: '/api/1.0/update_tweet.json',
      type: 'POST',
      contentType: 'application/JSON',
      data: JSON.stringify(send_vals),
      timeout: 10000,
      datatype: 'json'
    })
    .done(function(data){
        // alert(data['id']);
        _this.prev().find(".tweet-id").html(data['id'])
    })
    .fail(function(){
        _this.prev().find(".save-tweet").removeClass("text-secondary")
        _this.prev().find(".save-tweet").addClass("text-danger")
        alert("Failed.")
    })
})

var tweet_group_template = '<div class="my-2 tweet-group">' +
        '<h5 class="text-secondary">Tweet Group</h5>' +
        '<div class="p-2 my-1 border outline-secondary  rounded tweet-group-settings d-none shadow-sm">' +
            '<div class="text-right"><button class="btn btn-sm btn-secondary small set-tweet-group">Set</button></div>' +
            '<div class="tweet-group-setting-gid d-none"></div>' +
            '<div class="mb-1">Start: <input type="time" class="form-control form-control-sm sched-start-time" value="00:00:00" size="8"></div>' +
            '<div class="my-1">Interval: <input type="integer" class="form-control form-control-sm tweet-group-interval" value="60" size="3"></div>' +
            '<select class="form-control form-control-sm my-1 tweet-group-status"><option selected>DRAFT</option><option>SCHEDULED</option></select>' +
        '</div>' +
        '<div class="p-2 my-1 small border outline-secondary rounded tweet-group-settings-confirmed d-block shadow-sm">' +
            '<div class="text-right"><button class="btn btn-sm btn-secondary small edit-tweet-group">Edit</button> <button class="btn btn-sm btn-secondary small delete-tweet-group">Del</button> </div>' +
    '<div class="tweet-group-setting-gid d-none"></div>' +
            '<div class="mb-1">Start: <span class="sched-start-time">00:00:00</span></div>' +
            '<div class="my-1">Interval(sec): <span class="tweet-group-interval">60</span></div>' +
            '<div class="">Status: <span class="tweet-group-status">DRAFT</span></div>' +
        '</div>' +
        '<div class="border outline-secondary rounded text-center text-secondary add-tweet">+</div>' +
    '</div>'

$(document).on('click', ".add-tweet-group", function(){

    /* データ送信 */
    var send_vals = {}
    date_l = $(this).parent().find('.date').html() 
    send_vals.sched_start_date = date_l + ' ' + '00:00:00'
    send_vals.interval = 60

    _this =$(this)

    $.ajax({
      url:'api/1.0/add_tweet_group.json',
      type:'POST',
      contentType: 'application/JSON',
      data: JSON.stringify(send_vals),
      timeout: 10000,
      datatype: 'json'
    })
    .done(function(data){
        gid_l = data['gid']

        _this.before(tweet_group_template)
        _this.prev().find('.tweet-group-setting-gid').html(gid_l)
    })
    .fail(function(){
        alert("Failed.")
    })

})
