// Preload
$(window).on("load", function () {
    $(".preloader").fadeOut("slow");
});

$(document).ready(function () {
    $(".preloader").fadeOut("slow");
    burgerMenu('.burger-menu');
    loadOpenBets();
});

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

function loadOpenBets() {
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    $('.open_preloader').css("display", "flex");
    $.ajax({
        url: 'load-open-bets',
        type: 'POST',
        data: {},
        headers: {
            'X-CSRFToken': csrftoken
        },
        success: function(response) {
            $('.open_preloader').css("display", "none");
            const bets = JSON.parse(response.bets);
            if(bets.length > 0) {
                $('.open_empty').each(function() {
                    $(this).css("display", "none");
                });
            } else {
                $('.open_empty').each(function() {
                    $(this).css("display", "block");
                });
            }

            const balance = JSON.parse(response.balance);
            if(balance) {
                $('.balance').each(function() {
                    $(this).text(balance);
                });
            }
        },
        error: function(xhr, status, error) {
            console.error("AJAX Error:", error);
            $('.open_preloader').css("display", "flex");
        }
    });
}

// Create WebSocket connection.
const socket = new WebSocket("ws://127.0.0.1:8000/customer/");

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
