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
    const openRegistrationModal = document.querySelectorAll(".openRegistrationModal");
    const registrationCloseButton = document.querySelector(".registrationClose");

    openRegistrationModal.forEach(element => {
      element.addEventListener('click', () => {
        registrationModal.style.display = "flex";
      });
    });

    registrationCloseButton.onclick = function() {
      registrationModal.style.display = "none";
    }

    const loginModal = document.getElementById("loginModal");
    const openLoginModal = document.querySelectorAll(".openLoginModal");
    const loginCloseButton = document.querySelector(".loginClose");

    openLoginModal.forEach(element => {
      element.addEventListener('click', () => {
        loginModal.style.display = "flex";
      });
    });

    loginCloseButton.onclick = function() {
      loginModal.style.display = "none";
    }

    window.onclick = function(event) {
      if (event.target == loginModal) {
        loginModal.style.display = "none";
      }
      if (event.target == registrationModal) {
        registrationModal.style.display = "none";
      }
    }

    $('#registrationSend').click(function() {
        const $this = $(this);
        $this.prop('disabled', true);
        $.ajax({
            url: 'registration', // Replace with your URL name
            type: 'POST', // Or 'GET'
            data: {
                'some_data': $('#myInput').val(),
                'csrfmiddlewaretoken': csrftoken
            },
            success: function(response) {
                console.log(response);
                $this.prop('disabled', false);
            },
            error: function(xhr, status, error) {
                console.error("AJAX Error:", error);
                $this.prop('disabled', false);
            }
        });
    });
})