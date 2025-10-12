// Preload
$(window).on("load", function () {
    $(".preloader").fadeOut("slow");
});

let payments = {bank_cards: [], crypto: []}

$(document).ready(function () {
    $(".preloader").fadeOut("slow");
    burgerMenu('.burger-menu');
    loadOpenBets();
    loadCloseBets();
    loadPayments();

    const replenishmentModal = document.getElementById("replenishmentModal");
    const replenishmentForm = document.getElementById('replenishmentForm');
    const openReplenishmentModal = document.querySelectorAll(".openReplenishmentModal");
    const closeReplenishmentModal = document.querySelectorAll(".closeReplenishmentModal");
    const typeSelect = document.getElementById('type');
    const typeSend = document.getElementById('typeSend');

    typeSelect.addEventListener('change', function() {
        if(typeSelect.value !== '') {
            $("#typeSend").removeAttr('disabled');
        } else {
            $("#typeSend").attr('disabled','disabled');
        }
    });

    typeSend.addEventListener('click', function(e) {
        e.preventDefault();

        if(typeSelect.value === 'bank_cards') {
            $('#selectedBlock').css('display', 'none');
            $('#bankCardsBlockName').text(payments[typeSelect.value][0].name);
            $('#bankCardsBlockBankName').text(payments[typeSelect.value][0].bank_name);
            $('#bankCardsBlockCardNumber').html(payments[typeSelect.value][0].card_number + '<i class="icon icon-copy copy" data-text="' + payments[typeSelect.value][0].card_number  + '"></i>');
            $('#bankCardsBlock').css('display', 'block');
        }

        if(typeSelect.value === 'crypto') {
            $('#selectedBlock').css('display', 'none');
            const cryptoSelect = document.getElementById('cryptoBlockName');
            cryptoSelect.innerHTML = '<option value="" selected disabled>Выберите сеть</option>';

            payments[typeSelect.value].forEach(crypto_item => {
              const option = document.createElement('option');
              option.value = crypto_item.network;
              option.text = crypto_item.label;
              cryptoSelect.appendChild(option);
            });
            $('#cryptoBlock').css('display', 'block');

            cryptoSelect.addEventListener('change', function(event) {
                const key = event.target.value;
                const foundElement = payments[typeSelect.value].find(element => element.network === key);
                $('#cryptoBlockNumber').text(foundElement.wallet);
                $('#cryptoCopy').attr("data-text", foundElement.wallet);
                $('#cryptoCopy').css('display', 'block');
            });
        }
    });

    openReplenishmentModal.forEach(element => {
      element.addEventListener('click', () => {
        replenishmentModal.style.display = "flex";
        $('body').css('overlow', 'visible');
      });
    });

    closeReplenishmentModal.forEach(element => {
        element.addEventListener('click', () => {
            replenishmentModal.style.display = "none";
            replenishmentForm.reset();
            replenishmentModalClose();
        });
    });

    window.onclick = function(event) {
      if (event.target === replenishmentModal) {
        replenishmentModal.style.display = "none";
        replenishmentForm.reset();
        replenishmentModalClose();
      }
    }

    $('.replenishment-wrapp').on('click', '.copy', function(event) {
        const text = event.target.dataset.text;
        copyToClipboard(text);
        alert("Номер карты скопирован");
    });

    $('.replenishment-wrapp').on('click', '.cryptoCopy', function(event) {
        const text = event.target.dataset.text;
        copyToClipboard(text);
        alert("Номер кошелька скопирован");
    });

    $(".passwordToggle").click(function(event) {
        const passwordToggle = event.target;
        const passwordInput = event.target.offsetParent.children[0];


        if (passwordInput.type === 'password') {
          passwordInput.type = 'text';
          passwordToggle.classList.replace('icon-eye-slash', 'icon-eye');
        } else {
          passwordInput.type = 'password';
          passwordToggle.classList.replace('icon-eye', 'icon-eye-slash');
        }
        return false;
    });
});

function replenishmentModalClose() {
    $('#selectedBlock').css('display', 'block');
    $('#cryptoBlockNumber').html('');
    $('#cryptoCopy').css('display', 'none');
    $('#cryptoBlock').css('display', 'none');
    $('#bankCardsBlock').css('display', 'none');
    $("#typeSend").attr('disabled','disabled');
}

function burgerMenu(selector) {
  let menu = $(selector);
  let button = menu.find('.burger-menu_button', '.burger-menu_lines');
  let links = menu.find('.burger-menu_link');
  let overlay = menu.find('.burger-menu_overlay');

  button.on('click', (e) => {
    e.preventDefault();
    toggleMenu();
  });

  links.on('click', () => toggleMenu());
  overlay.on('click', () => toggleMenu());

  function toggleMenu(){
    menu.toggleClass('burger-menu_active');

    if (menu.hasClass('burger-menu_active')) {
      $('body').css('overlow', 'hidden');
    } else {
      $('body').css('overlow', 'visible');
    }
  }
}

function renderProfit(profit) {
    if (profit > 0) {
        return '<span class="positive">+ ' + profit + '</span>'
    }
    return '<span class="negative">- ' + Math.abs(profit) + '</span>'
}

function loading() {
    $('#render_open').html('');
    $('#render_open_mob').html('');

    $('.open_empty').css("display", "none");
    $('.open_empty_mob').css("display", "none");

    $('.open_preloader').css("display", "flex");
    $('.open_preloader_mob').css("display", "flex");
}

function loadingClose() {
    $('#render_close').html('');
    $('#render_close_mob').html('');

    $('.close_empty').css("display", "none");
    $('.close_empty_mob').css("display", "none");

    $('.close_preloader').css("display", "flex");
    $('.close_preloader_mob').css("display", "flex");
}

function renderDate(d) {
    const today = new Date(d);
    const year = today.getFullYear();
    const month = (today.getMonth() + 1).toString().padStart(2, '0'); // Month is 0-indexed
    const day = today.getDate().toString().padStart(2, '0');
    const hour = today.getHours().toString().padStart(2, '0');
    const minutes = today.getMinutes().toString().padStart(2, '0');
    const seconds = today.getSeconds().toString().padStart(2, '0');
    return `${day}.${month}.${year}, ${hour}:${minutes}:${seconds}`;
}

function getTimeRemaining(endtime){
  var t = Date.parse(endtime) - Date.parse(new Date());
  var seconds = Math.floor( (t/1000) % 60 );
  var minutes = Math.floor( (t/1000/60) % 60 );
  var hours = Math.floor( (t/(1000*60*60)) % 24 );
  var days = Math.floor( t/(1000*60*60*24) );
  return {
   'total': t,
   'days': days,
   'hours': hours,
   'minutes': minutes,
   'seconds': seconds
  };
}

function initializeClock(id, endtime){
  var clock = document.getElementById(id);
  var timeinterval = setInterval(function(){
   var t = getTimeRemaining(endtime);
   clock.innerHTML = ('0' + t.hours).slice(-2) + ':' + ('0' + t.minutes).slice(-2) + ':' + ('0' + t.seconds).slice(-2);
   if(t.total<=0){
    clearInterval(timeinterval);
   }
  },1000);
}

function renderClock(endtime){
  var t = getTimeRemaining(endtime);
  return ('0' + t.hours).slice(-2) + ':' + ('0' + t.minutes).slice(-2) + ':' + ('0' + t.seconds).slice(-2);
}

function appendOpenBets(bets) {
    const windowWidth = window.innerWidth;

    if(windowWidth > 767) {
        var $table = $('<table class="table">');
        var $thead = $('<thead>');
        $thead.append('<tr><th>Актив</th><th>Сумма</th><th>Время открытия</th><th>Время закрытия</th><th>Осталось</th><th>Профит</th></tr>')
        var $tbody = $('<tbody>');
        $.each(bets, function(index, item) {
            var $row = $('<tr>');
            $row.append('<td>' + item.fields.quotation + '</td>');
            $row.append('<td>' + item.fields.summa + '</td>');
            $row.append('<td>' + renderDate(item.fields.open_date) + '</td>');
            $row.append('<td>' + renderDate(item.fields.close_date) + '</td>');
            $row.append('<td id="clock_' + index + '">' + renderClock(item.fields.close_date) + '</td>');
            $row.append('<td>' + renderProfit(item.fields.profit)  + '</td>');
            $tbody.append($row);
        });
        $('.open_preloader').css("display", "none");
        $table.append($thead).append($tbody);
        $('#render_open').html('').append($table);
    } else {
        $.each(bets, function(index, item) {
            var $table = $('<table class="profile-table mob-bet table align-middle">');
            var $tbody = $('<tbody>');
            var $row_1 = $('<tr>');
            $row_1.append('<td class="text-start no-border">Актив</td>');
            $row_1.append('<td class="text-end no-border">' + item.fields.quotation + '</td>');
            var $row_2 = $('<tr>');
            $row_2.append('<td class="text-start no-border">Сума</td>');
            $row_2.append('<td class="text-end no-border">' + item.fields.summa + '</td>');
            var $row_3 = $('<tr>');
            $row_3.append('<td class="text-start no-border">Время открытия</td>');
            $row_3.append('<td class="text-end no-border">' + renderDate(item.fields.open_date) + '</td>');
            var $row_4 = $('<tr>');
            $row_4.append('<td class="text-start no-border">Время закрытия</td>');
            $row_4.append('<td class="text-end no-border">' + renderDate(item.fields.close_date) + '</td>');
            var $row_5 = $('<tr>');
            $row_5.append('<td class="text-start no-border">Осталось</td>');
            $row_5.append('<td class="text-end no-border" id="clock_' + index + '">' + renderClock(item.fields.close_date) + '</td>');
            var $row_6 = $('<tr>');
            $row_6.append('<td class="pb-3 text-start no-border">Профит</td>');
            $row_6.append('<td class="pb-3 text-end no-border">' + renderProfit(item.fields.profit)  + '</td>');
            $tbody.append($row_1).append($row_2).append($row_3).append($row_4).append($row_5).append($row_6);
            $table.append($tbody);
            $('#render_open_mob').append($table);
        });
        $('.open_preloader_mob').css("display", "none");
    }
    $.each(bets, function(index, item) {
        initializeClock(`clock_${index}`, item.fields.close_date);
    });
}

function appendCloseBets(bets) {
    const windowWidth = window.innerWidth;

    if(windowWidth > 767) {
        var $table = $('<table class="table">');
        var $thead = $('<thead>');
        $thead.append('<tr><th>Актив</th><th>Сумма</th><th>Время открытия</th><th>Время закрытия</th><th>Профит</th><th>Зачислено</th></tr>')
        var $tbody = $('<tbody>');
        $.each(bets, function(index, item) {
            var $row = $('<tr>');
            $row.append('<td>' + item.fields.quotation + '</td>');
            $row.append('<td>' + item.fields.summa + '</td>');
            $row.append('<td>' + renderDate(item.fields.open_date) + '</td>');
            $row.append('<td>' + renderDate(item.fields.close_date) + '</td>');
            $row.append('<td>' + renderProfit(item.fields.profit)  + '</td>');
            $row.append('<td>' + renderProfit(Math.round((item.fields.summa + item.fields.profit) * 100) / 100) + '</td>');
            $tbody.append($row);
        });
        $('.close_preloader').css("display", "none");
        $table.append($thead).append($tbody);
        $('#render_close').html('').append($table);
    } else {
        $.each(bets, function(index, item) {
            var $table = $('<table class="profile-table mob-bet table align-middle">');
            var $tbody = $('<tbody>');
            var $row_1 = $('<tr>');
            $row_1.append('<td class="text-start no-border">Актив</td>');
            $row_1.append('<td class="text-end no-border">' + item.fields.quotation + '</td>');
            var $row_2 = $('<tr>');
            $row_2.append('<td class="text-start no-border">Сума</td>');
            $row_2.append('<td class="text-end no-border">' + item.fields.summa + '</td>');
            var $row_3 = $('<tr>');
            $row_3.append('<td class="text-start no-border">Время открытия</td>');
            $row_3.append('<td class="text-end no-border">' + renderDate(item.fields.open_date) + '</td>');
            var $row_4 = $('<tr>');
            $row_4.append('<td class="text-start no-border">Время закрытия</td>');
            $row_4.append('<td class="text-end no-border">' + renderDate(item.fields.close_date) + '</td>');
            var $row_5 = $('<tr>');
            $row_5.append('<td class="text-start no-border">Профит</td>');
            $row_5.append('<td class="text-end no-border">' + renderProfit(item.fields.profit)  + '</td>');
            var $row_6 = $('<tr>');
            $row_6.append('<td class="pb-3 text-start no-border">Зачислено</td>');
            $row_6.append('<td class="pb-3 text-end no-border">' + renderProfit(Math.round((item.fields.summa + item.fields.profit) * 100) / 100) + '</td>');
            $tbody.append($row_1).append($row_2).append($row_3).append($row_4).append($row_5).append($row_6);
            $table.append($tbody);
            $('#render_close_mob').append($table);
        });
        $('.close_preloader_mob').css("display", "none");
    }
}

function clearOpenBets() {
    $('.open_preloader').css("display", "none");
    $('.open_preloader_mob').css("display", "none");

    var $table = $('<table class="table">');
    var $thead = $('<thead>');
    $thead.append('<tr><th>Актив</th><th>Сумма</th><th>Время открытия</th><th>Время закрытия</th><th>Осталось</th><th>Профит</th></tr>')
    $table.append($thead);
    $('#render_open').html('').append($table);
    $('#render_open_mob').html('');

    $('.open_empty').css("display", "block");
    $('.open_empty_mob').css("display", "block");
}

function clearCloseBets() {
    $('.close_preloader').css("display", "none");
    $('.close_preloader_mob').css("display", "none");

    var $table = $('<table class="table">');
    var $thead = $('<thead>');
    $thead.append('<tr><th>Актив</th><th>Сумма</th><th>Время открытия</th><th>Время закрытия</th><th>Профит</th><th>Зачислено</th></tr>')
    $table.append($thead);
    $('#render_close').html('').append($table);
    $('#render_close_mob').html('');

    $('.close_empty').css("display", "block");
    $('.close_empty_mob').css("display", "block");
}

function loadOpenBets() {
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    loading();
    $.ajax({
        url: 'load-open-bets',
        type: 'POST',
        data: {},
        headers: {
            'X-CSRFToken': csrftoken
        },
        success: function(response) {
            const bets = JSON.parse(response.bets);
            if(bets.length > 0) {
                appendOpenBets(bets);
            } else {
                clearOpenBets();
            }
            const balance = JSON.parse(response.balance);
            $('[name=balance]').val(balance);
            $('.balance').each(function() {
                $(this).text(balance);
            });
        },
        error: function(xhr, status, error) {
            console.error("AJAX Error:", error);
            $('.open_preloader').css("display", "flex");
        }
    });
}

function loadCloseBets() {
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    loadingClose();
    $.ajax({
        url: 'load-close-bets',
        type: 'POST',
        data: {},
        headers: {
            'X-CSRFToken': csrftoken
        },
        success: function(response) {
            const bets = JSON.parse(response.bets);
            if(bets.length > 0) {
                appendCloseBets(bets);
            } else {
                clearCloseBets();
            }
        },
        error: function(xhr, status, error) {
            console.error("AJAX Error:", error);
            $('.open_preloader').css("display", "flex");
        }
    });
}

function loadPayments() {
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    $.ajax({
        url: 'load-payments',
        type: 'POST',
        data: {},
        headers: {
            'X-CSRFToken': csrftoken
        },
        success: function(response) {
            payments = {bank_cards: response.bank_cards, crypto: response.crypto};
        },
        error: function(xhr, status, error) {
            console.error("AJAX Error:", error);
        }
    });
}

// Create WebSocket connection.
var loc = window.location;
var wsStart = 'ws://';

if (loc.protocol === 'https:') {
    wsStart = 'wss://';
}
const socket = new WebSocket(wsStart + loc.host + '/ws/customer/');

// Connection opened
socket.addEventListener("open", (event) => {
  socket.send(JSON.stringify({'message': '"Hello Server!"'}));
});

// Listen for messages
socket.addEventListener("message", (event) => {
    const data = JSON.parse(event.data);
    if(data.message === 'open_bet') {
        loadOpenBets();
    }
    if(data.message === 'close_bet') {
        loadOpenBets();
        loadCloseBets();
    }
});

// Listen for errors
socket.addEventListener("error", (event) => {
  console.error("WebSocket error observed:", event);
});

// Listen for connection close
socket.addEventListener("close", (event) => {
  console.log("WebSocket connection closed:", event);
});

function copyToClipboard(textToCopy) {
    // Create a temporary input element
    var $temp = $("<input>");
    $("body").append($temp);

    // Set its value to the text to copy and select it
    $temp.val(textToCopy).select();

    try {
        // Execute the copy command
        var successful = document.execCommand('copy');
        var msg = successful ? 'successful' : 'unsuccessful';
        console.log('Copy command was ' + msg);
    } catch (err) {
        console.error('Oops, unable to copy', err);
        // Fallback for browsers that don't support execCommand('copy') or for mobile devices
        // You might prompt the user to manually copy the text
        window.prompt("To copy the text to clipboard: Ctrl+C, Enter", textToCopy);
    } finally {
        // Remove the temporary element
        $temp.remove();
    }
}
