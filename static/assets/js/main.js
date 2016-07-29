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

yArr = [
    [[10, 'q'], [20, 'w'], [30, 'e'], [40, 'r'], [50, 't'], [60, 'y'], [70, 'u'], [80, 'i'], [90, 'o'], [100, 'p']],
    [[15, 'a'], [25, 's'], [35, 'd'], [45, 'f'], [55, 'g'], [65, 'h'], [75, 'j'], [85, 'k'], [100, 'l']],
    [[13.8, 'shift'], [25.5, 'z'], [35.5, 'x'], [45.5, 'c'], [55.5, 'v'], [65.5, 'b'], [75.5, 'n'], [85.5, 'm'], [100, 'bkspace']],
    [[12.5, '123'], [25.5, 'globe'], [35.5, 'mic'], [75.5, 'space'], [100, 'return']]
];


var ctrl = {
    tempResult: [],
    temp: {},
    input: '',
    shift: false,
    init: function () {

        $('#keyboardContainer').css({top: keyboardMarginTop});


        $('#keyboardContainer').on('touchstart', function (event) {
            ctrl.prepare(event);
        });
        $('#keyboardContainer').on('touchend', function (event) {
            ctrl.record(event);
        });
    },
    prepare: function (e) {
        var oe = e.originalEvent;
        console.log(oe);

        var x = oe.changedTouches[0].clientX / keyboardWidth * 100;
        var y = (oe.changedTouches[0].clientY - keyboardMarginTop) / keyboardHeight * 100;
        // console.log(x / keyboardWidth * 100, y / keyboardHeight * 100);

        var letter = '';
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
        var downResult = {
            x: x,
            y: y,
            time: oe.timeStamp,
        };

        ctrl.temp[letter] = downResult;
    },
    record: function (e) {
        // console.log(e);
        var oe = e.originalEvent;
        console.log(oe);

        var x = oe.changedTouches[0].clientX / keyboardWidth * 100;
        var y = (oe.changedTouches[0].clientY - keyboardMarginTop) / keyboardHeight * 100;
        // console.log(x / keyboardWidth * 100, y / keyboardHeight * 100);

        var letter = '';
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


        if (letter != 'bkspace' && letter != 'shift' && letter != 'globe' && letter != 'mic' && letter != 'return' && letter != 'space') {
            ctrl.input += letter;
            $('#replacehere').val(ctrl.input);

        } else if (letter == 'space') {
            ctrl.input += ' ';
            $('#replacehere').val(ctrl.input);
        } else if (letter == 'bkspace') {
            ctrl.input = ctrl.input.substring(0, ctrl.input.length - 1);
            $('#replacehere').val(ctrl.input);
        }


        var downResult = _.clone(ctrl.temp[letter]);
        ctrl.temp[letter] = null;

        if (!downResult){
            return;
        }


        var upResult = {
            x: x,
            y: y,
            time: oe.timeStamp,
        }

        var result = {
            up: upResult,
            down: downResult,
            letter: letter
        };

        ctrl.tempResult.push(result);


        if (result.letter == 'return') {

            var finalResult = {
                data: ctrl.tempResult,
                id: '1',
                imposter: 'false',
                text: ctrl.input
            }

            console.log('result', finalResult);
            $('#resulthere').val(JSON.stringify(finalResult));

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
                data: JSON.stringify(finalResult),
                dataType: 'json',
                success: function (res) {
                    console.log(res);
                },
                error: function (err) {
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



