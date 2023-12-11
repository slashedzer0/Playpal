function toggle_regis_talent() {
  $("#regiscustomer-box").toggleClass("visually-hidden");
  $("#registalent-box").toggleClass("visually-hidden");
}

function register_customer() {
  let fullname = $("#fullname-customer").val();
  let username = $("#username-customer").val();
  let password = $("#password-customer").val();

  if (fullname === "") {
    $("#help-customer")
      .text("Please fill in fullname")
      .removeClass("invisible");
    $("#fullname-customer").focus();
    return;
  } else if (username === "") {
    $("#help-customer")
      .text("Please fill in username")
      .removeClass("invisible");
    $("#username-customer").focus();
    return;
  } else if (password === "") {
    $("#help-customer")
      .text("Please fill in password")
      .removeClass("invisible");
    $("#password-customer").focus();
    return;
  } else if (!/^[a-zA-Z0-9]{1,15}$/.test(username)) {
    $("#help-customer")
      .text(
        "Invalid username, only alphanumeric characters are allowed (max 15 characters)"
      )
      .removeClass("invisible");
    $("#username-customer").focus();
    return;
  }

  $.ajax({
    type: "POST",
    url: "/api/register_customer",
    data: {
      fullname: fullname,
      username: username,
      password: password,
    },
    success: function (response) {
      exists = response["exists"];
      console.log(response);
      if (exists) {
        $("#help-customer")
          .text("Username already exists")
          .removeClass("invisible");
        return;
      }
      window.location.replace("/login");
    },
  });
}

function register_talent() {
  let fullname = $("#fullname-talent").val();
  let username = $("#username-talent").val();
  let password = $("#password-talent").val();
  let game = $("#game").val();
  let price = $("#price").val();

  if (fullname === "") {
    $("#help-talent").text("Please fill in fullname").removeClass("invisible");
    $("#fullname-talent").focus();
    return;
  } else if (username === "") {
    $("#help-talent").text("Please fill in username").removeClass("invisible");
    $("#username-talent").focus();
    return;
  } else if (password === "") {
    $("#help-talent").text("Please fill in password").removeClass("invisible");
    $("#password-talent").focus();
    return;
  } else if (game === "") {
    $("#help-talent").text("Please select a game").removeClass("invisible");
    $("#game").focus();
    return;
  } else if (price === "") {
    $("#help-talent")
      .text("Please select a unit price")
      .removeClass("invisible");
    $("#price").focus();
    return;
  } else if (!/^[a-zA-Z0-9]{1,15}$/.test(username)) {
    $("#help-talent")
      .text(
        "Invalid username, only alphanumeric characters are allowed (max 15 characters)"
      )
      .removeClass("invisible");
    $("#username-talent").focus();
    return;
  }

  $.ajax({
    type: "POST",
    url: "/api/register_talent",
    data: {
      fullname: fullname,
      username: username,
      password: password,
      game: game,
      price: price,
    },
    success: function (response) {
      exists = response["exists"];
      console.log(response);
      if (exists) {
        $("#help-talent")
          .text("Username already exists")
          .removeClass("invisible");
        return;
      }
      window.location.replace("/login");
    },
  });
}

function login() {
  let username = $("#username").val();
  let password = $("#password").val();

  if (username === "") {
    $("#help-login").text("Please fill in username").removeClass("invisible");
    $("#username").focus();
    return;
  } else if (password === "") {
    $("#help-login").text("Please fill in password").removeClass("invisible");
    $("#password").focus();
    return;
  }

  $.ajax({
    type: "POST",
    url: "/api/login",
    data: {
      username: username,
      password: password,
    },
    success: function (response) {
      console.log(response)
      if (response["result"] === "success") {
        $.cookie("token", response["token"], { path: "/" });
        window.location.replace("/");
      } else {
        alert(response["msg"]);
      }
    },
  });
}

function sign_out() {
  $.removeCookie("token", { path: "/" });
  window.location.href = "/login";
}

