// Preload
$(window).on("load", function () {
    $(".preloader").fadeOut("slow");
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

  $(window).scroll(function() {
      menu.removeClass('burger-menu_active');
      $('body').css('overlow', 'visible');
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

burgerMenu('.burger-menu');

$(document).ready(function () {
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    $.scrollIt({
        topOffset: -50
    });

    let menu = $('.burger-menu');
    const registrationModal = document.getElementById("registrationModal");
    const registrationForm = document.getElementById('registrationForm');
    const openRegistrationModal = document.querySelectorAll(".openRegistrationModal");
    const registrationCloseButton = document.querySelector(".registrationClose");

    openRegistrationModal.forEach(element => {
      element.addEventListener('click', () => {
        registrationModal.style.display = "flex";

        menu.removeClass('burger-menu_active');
        $('body').css('overlow', 'visible');
      });
    });

    registrationCloseButton.onclick = function() {
      registrationModal.style.display = "none";
      registrationForm.reset();
    }

    const loginModal = document.getElementById("loginModal");
    const forgotPasswordForm = document.getElementById("forgotPasswordForm");
    const loginForm = document.getElementById('loginForm');
    const openLoginModal = document.querySelectorAll(".openLoginModal");
    const loginCloseButton = document.querySelector(".loginClose");

    openLoginModal.forEach(element => {
      element.addEventListener('click', () => {
        loginModal.style.display = "flex";

        menu.removeClass('burger-menu_active');
        $('body').css('overlow', 'visible');
      });
    });

    loginCloseButton.onclick = function() {
      loginModal.style.display = "none";
      loginForm.style.display = "block";
      forgotPasswordForm.style.display = "none";
      loginForm.reset();
    }

    window.onclick = function(event) {
      if (event.target == loginModal) {
        loginModal.style.display = "none";
        loginForm.style.display = "block";
        forgotPasswordForm.style.display = "none";
        loginForm.reset();
      }
      if (event.target == registrationModal) {
        registrationModal.style.display = "none";
        registrationForm.reset();
      }
    }

    $('#registrationForm').on('submit', function(event) {
        event.preventDefault();
        $('#registrationSend').prop('disabled', true);

        $.ajax({
            url: 'registration',
            type: 'POST',
            data: $(this).serialize(),
            headers: {
                'X-CSRFToken': csrftoken
            },
            success: function(response) {
                $('#registrationSend').prop('disabled', false);
                registrationForm.reset();
                registrationModal.style.display = "none";
            },
            error: function(xhr, status, error) {
                console.error("AJAX Error:", error);
                $('#registrationSend').prop('disabled', false);
            }
        });
    });

    $('#loginForm').on('submit', function(event) {
        event.preventDefault();
        $('#loginSend').prop('disabled', true);

        $.ajax({
            url: 'login',
            type: 'POST',
            data: $(this).serialize(),
            headers: {
                'X-CSRFToken': csrftoken
            },
            success: function() {
                loginForm.reset();
                window.location.href = "/profile";
            },
            error: function(xhr, status) {
                console.error("AJAX Error:", status, xhr?.responseJSON.error);
                $('#loginSend').prop('disabled', false);
            }
        });
    });

    $("#showForgotPasswordForm").click(function(event) {
        $('#loginForm').css('display', 'none');
        $('#forgotPasswordForm').css('display', 'block');
        return false;
      });
});