var send;
$(function(){

    function send_code(code) {
        // because if different server, I need to use JSONP
        $.ajax({
            type: 'GET',
            url: '/api/to_bytecode',
            data: {'code': window.JSON.stringify(code)},
            dataType: 'jsonp',
            success: function(data) {
                console.log(data);
                update_bytecode(data);
            }
        });
    }

    var code = $('#code').val();
    send_code(code);

    function check_input(){
        var new_code = $('#code').val();
        if(new_code != code){
            code = new_code;
            send_code(code);
        }
    }
    setInterval(check_input, 1000);

    function update_bytecode(data){
        if(data == null) return;
        if(data['error'] != null){
            $('#error').text(data['error']);
            return;
        }else{
            $('#error').text('');
        }
        $('#bytecode').empty();
        $('#bytecode').append($('<colgroup span="3"></colgroup><colgroup span=5 style="background-color:#eee;"></colgroup>'));
        $('#bytecode').append($('<tr><th>line</th><th>opname</th><th>argument</th><th colspan=5>debug info</th></tr>'));
        console.log(data);
        // tableの方が揃えやすくていいかも
        data.forEach(function(line){
            var line_no = line['line_no'];
            if(line_no != null){
                var tr = $("<tr>");
                var td = $("<td>");
                td.text(line_no);
                tr.append(td);
                td = $("<td colspan=7>");
                td.text(code.split("\n")[line_no - 1]);
                tr.append(td);
                $('#bytecode').append(tr);
            }
            //var item = $('<li id="' + line['i'] + '">');
            //console.log(line['i'])
            //item.html(line['i']);

            var tr = $("<tr>");
            function push(v){
                var td = $("<td>");
                td.text(v);
                tr.append(td);
                return td;
            }

            push(''); // line_no
            var opname = line['opname'];
            push(opname);

            // make human-readable form of argument
            USE_RAW = ['CALL_FUNCTION', 'POP_JUMP_IF_FALSE',
                       'JUMP_ABSOLUTE'];
            var arg = '';
            if(line['arg']){
                arg = line['arg']['value'];
            }else if(USE_RAW.some(function(x){return opname == x})){
                arg = line['raw_arg'];
            }
            push(arg);

            if(line['in_labels']){
                push('>> ');
            }else{
                push('   ');
            }
            push(line['i']);
            push(line['hex']);
            push(line['raw_op']);

            push(line['raw_arg']);
            $('#bytecode').append(tr);
        })
    }
})