// $(function () {
/*// jquery keyboard plugin
 jsKeyboard.init("virtualKeyboard");

 //first input focus
 var $firstInput = $(':input').first().focus();
 jsKeyboard.currentElement = $firstInput;
 jsKeyboard.currentElementCursorPosition = 0;*/
// });


// put keyboard at bottom

// var serverUrl = 'http://10.130.26.28:8080/';
var serverUrl = 'http://128.199.195.84:3000/';
// var serverUrl = 'http://localhost:80/';

var ctrl = {
    tempResult: [],
    init: function () {

        $('#keyboardContainer').css({top: keyboardMarginTop});


        $('#keyboardContainer').on('touchstart', function (event) {
            ctrl.record(event);
        });
    },
    record: function (e) {
        // console.log(e);
        var oe = e.originalEvent;
        console.log(oe);

        var x = oe.changedTouches[0].clientX;
        var y = oe.changedTouches[0].clientY - keyboardMarginTop;
        // console.log(x / keyboardWidth * 100, y / keyboardHeight * 100);

        x = x / keyboardWidth * 100
        y = y / keyboardHeight * 100
        var letter = '';


        //TODO: FILL UP LETTER!
        yArr = [
            [[10, 'q'], [20, 'w'], [30, 'e'], [40, 'r'], [50, 't'], [60, 'y'], [70, 'u'], [80, 'i'], [90, 'o'], [100, 'p']],
            [[15, 'a'], [25, 's'], [35, 'd'], [45, 'f'], [55, 'g'], [65, 'h'], [75, 'j'], [85, 'k'], [100, 'l']],
            [[13.8, 'shift'], [25.5, 'z'], [35.5, 'x'], [45.5, 'c'], [55.5, 'v'], [65.5, 'b'], [75.5, 'n'], [85.5, 'm'], [100, 'bkspace']],
            [[12.5, '123'], [25.5, 'globe'], [35.5, 'mic'], [75.5, 'space'], [100, 'return']]
        ];

        xArr = [];
        if (y <= 25) {
            xArr = yArr[0]
        } else if (y <= 50) {
            xArr = yArr[1]
        } else if (y <= 75) {
            xArr = yArr[2]
        } else if (y <= 100) {
            xArr = yArr[3]
        }

        for (var i = 0; i < xArr.length; i++) {
            var xCoord = xArr[i][0];
            if (x < xCoord) {
                letter = xArr[i][1];
                break;
            }
        }


        console.log(letter);
        var result = {
            x: x,
            y: y,
            time: oe.timeStamp,
            letter: letter
        }
        ctrl.tempResult.push(result);
        if (result.letter == 'return') {
            console.log('result', ctrl.tempResult);
            $('#resulthere').val(JSON.stringify(ctrl.tempResult));

            var csrftoken = '';
            var cookies = document.cookie.split(';');
            _.map(cookies, function (cookie) {
                var keyValue = cookie.split('=');
                if (keyValue[0].trim() == 'csrftoken') {
                    csrftoken = keyValue[1];
                };
            });


            $.ajax({
                url: '/api/saveResult',
                beforeSend: function (xhr) {
                    xhr.setRequestHeader('X-CSRFToken', csrftoken);
                },
                type: 'POST',
                data: JSON.stringify(ctrl.tempResult),
                dataType: 'json',
                success: function(res){
                    console.log(res);
                },
                error: function(err){
                    console.log(err);
                }
            });

        }
        console.log(result);

    }
};

$(document).ready(function () {
    windowHeight = $(window).height();
    keyboard = $('#keyboardContainer');
    keyboardHeight = keyboard.height();
    keyboardWidth = keyboard.width();
    keyboardMarginTop = windowHeight - keyboardHeight;
    ctrl.init();
});



