// Preload
$(window).on("load", function () {
    $(".preloader").fadeOut("slow");
});

$(document).ready(function () {
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    $.scrollIt({
        topOffset: -50
    });

    const registrationModal = document.getElementById("registrationModal");
    const registrationForm = document.getElementById('registrationForm');
    const openRegistrationModal = document.querySelectorAll(".openRegistrationModal");
    const registrationCloseButton = document.querySelector(".registrationClose");

    openRegistrationModal.forEach(element => {
      element.addEventListener('click', () => {
        registrationModal.style.display = "flex";
      });
    });

    registrationCloseButton.onclick = function() {
      registrationModal.style.display = "none";
      registrationForm.reset();
    }

    const loginModal = document.getElementById("loginModal");
    const loginForm = document.getElementById('loginForm');
    const openLoginModal = document.querySelectorAll(".openLoginModal");
    const loginCloseButton = document.querySelector(".loginClose");

    openLoginModal.forEach(element => {
      element.addEventListener('click', () => {
        loginModal.style.display = "flex";
      });
    });

    loginCloseButton.onclick = function() {
      loginModal.style.display = "none";
      loginForm.reset();
    }

    window.onclick = function(event) {
      if (event.target == loginModal) {
        loginModal.style.display = "none";
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
})