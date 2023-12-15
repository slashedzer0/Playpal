function toggle_register_form() {
  $("#form-customer").toggleClass("visually-hidden");
  $("#form-talent").toggleClass("visually-hidden");
}

function register_customer() {
  let fullname = $("#fullname-customer").val();
  let username = $("#username-customer").val();
  let password = $("#password-customer").val();

  if (fullname === "") {
    $("#help-customer")
      .text("Please type in fullname")
      .removeClass("invisible");
    $("#fullname-customer").focus();
    return;
  } else if (username === "") {
    $("#help-customer")
      .text("Please type in username")
      .removeClass("invisible");
    $("#username-customer").focus();
    return;
  } else if (password === "") {
    $("#help-customer")
      .text("Please type in password")
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
  let unit = $("#price").find(":selected").text();

  if (fullname === "") {
    $("#help-talent").text("Please type in fullname").removeClass("invisible");
    $("#fullname-talent").focus();
    return;
  } else if (username === "") {
    $("#help-talent").text("Please type in username").removeClass("invisible");
    $("#username-talent").focus();
    return;
  } else if (password === "") {
    $("#help-talent").text("Please type in password").removeClass("invisible");
    $("#password-talent").focus();
    return;
  } else if (game === "") {
    $("#help-talent").text("Game cannot be empty").removeClass("invisible");
    $("#game").focus();
    return;
  } else if (price === "") {
    $("#help-talent")
      .text("Unit price cannot be empty")
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
      unit: unit,
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
  $(document);

  let username = $("#username").val();
  let password = $("#password").val();

  if (username === "") {
    $("#help-login").text("Please type in username").removeClass("invisible");
    $("#username").focus();
    return;
  } else if (password === "") {
    $("#help-login").text("Please type in password").removeClass("invisible");
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
      console.log(response);
      if (response["result"] === "success") {
        $.cookie("token", response["token"], { path: "/" });
        window.location.replace("/");
      } else {
        $("#help-login")
          .text("Invalid username or incorrect password")
          .removeClass("invisible");
        $("#username").focus();
      }
    },
  });
}

function sign_out() {
  $.removeCookie("token", { path: "/" });
  window.location.reload();
  window.location.href = "/login";
}

function delete_account() {
  $.ajax({
    type: "POST",
    url: "/api/delete_account",
    data: {
      token: $.cookie("token"),
    },
    success: function (response) {
      console.log(response);
      if (response["result"] === "success") {
        sign_out();
      }
    },
  });
}

function update_account() {
  let fullname = $("#fullname").val();
  let username = $("#username").val();
  let avatar = $("#avatar")[0].files[0];

  let form_data = new FormData();
  form_data.append("fullname", fullname);
  form_data.append("username", username);
  form_data.append("avatar", avatar);

  $.ajax({
    type: "POST",
    url: "/api/update_account",
    data: form_data,
    cache: false,
    contentType: false,
    processData: false,
    success: function (response) {
      console.log(response);
      if (response["result"] === "success") {
        window.location.reload();
      }
    },
  });
}

function update_talent() {
  let game = $("#game").val();
  let price = $("#price").val();
  let unit = $("#price").find(":selected").text();
  let rank = $("#rank").val();
  let since = $("#since").val();
  let region = $("#region").val();
  let platform = $("#platform").val();

  $.ajax({
    type: "POST",
    url: "/api/update_talent",
    data: {
      game: game,
      price: price,
      unit: unit,
      rank: rank,
      since: since,
      region: region,
      platform: platform,
    },
    success: function (response) {
      console.log(response);
      if (response["result"] === "success") {
        window.location.reload();
      }
    },
  });
}

function create_order() {
  let username_customer = $("#username").val();
  let username_talent = $("#username-talent").text();
  let game = $("#game-talent").text();
  let quantity = $("#quantity").val();
  let payment = $("#payment").val();
  let note = $("#note").val();

  if (quantity === "") {
    $("#quantity").focus();
    return;
  } else if (payment === "") {
    $("#payment").focus();
    return;
  } else {
    $("#form-order").fadeOut(500, function () {
      $("#success-order").fadeIn(500);
    });
  }

  $.ajax({
    type: "POST",
    url: "/api/create_order",
    data: {
      customer: username_customer,
      talent: username_talent,
      game: game,
      quantity: quantity,
      payment: payment,
      note: note,
    },
    success: function (response) {
      console.log(response);
      if (response["result"] === "success") {
        console.log("Order created");
      }
    },
  });
}

function load_customer_history() {
  $.ajax({
    type: "GET",
    url: "/api/load_customer_history",
    data: {},
    success: function (response) {
      console.log(response);
      if (response["result"] === "success") {
        created_orders = response["created_orders"];

        for (let i = 0; i < created_orders.length; i++) {
          let count = i + 1;
          let order = created_orders[i];
          let order_id = order.order_id;
          let game = order.game;
          let quantity = order.quantity;
          let payment = order.payment;
          let status = order.status;

          if (status == "waiting") {
            status = '<td class="text-secondary">WAITING</td><td></td>';
          } else if (status == "done") {
            status =
              '<td class="text-success">DONE</td><td> <a class="btn btn-dark" onclick="proceed_review(' +
              i +
              ')">ADD REVIEW</a></td>';
          } else if (status == "completed") {
            status = '<td class="text-primary">COMPLETED</td><td></td>';
          } else if (status == "declined") {
            status = '<td class="text-danger">DECLINED</td><td></td>';
          } else if (status == "pending") {
            status =
              '<td class="text-warning">PENDING</td><td> <a onclick="complete_order(' +
              i +
              ')" class="btn btn-dark">DONE</a></td>';
          } else {
            status = '<td class="text-dark">UNKNOWN</td><td></td>';
          }

          let temp_html = `
          <tr>
            <td>${count}</td>
            <td id="order-id-${count}">${order_id}</td>
            <td>${game}</td>
            <td>${quantity}</td>
            <td>${payment}</td>
            ${status}
          </tr>
          `;
          $("#customer-history").append(temp_html);
        }
      }
    },
  });
}

function load_talent_orders() {
  $.ajax({
    type: "GET",
    url: "/api/load_talent_orders",
    data: {},
    success: function (response) {
      console.log(response);
      if (response["result"] === "success") {
        received_orders = response["received_orders"];

        for (let i = 0; i < received_orders.length; i++) {
          let count = i + 1;
          let order = received_orders[i];
          let order_id = order.order_id;
          let quantity = order.quantity;
          let payment = order.payment;
          let note = order.note;
          let status = order.status;

          if (status == "waiting") {
            status =
              '<td><a onclick="approve_order(' +
              i +
              ')" class="btn btn-success">APPROVE</a>&nbsp;&nbsp;<a onclick="decline_order(' +
              i +
              ')" class="btn btn-danger">DECLINE</a></td>';
          }

          let temp_html = `
          <tr>
            <td>${count}</td>
            <td id="order-id-${count}">${order_id}</td>
            <td>${quantity}</td>
            <td>${payment}</td>
            <td>${note}</td>
            ${status}
          </tr>
          `;
          $("#talent-orders").append(temp_html);
        }
      }
    },
  });
}

function approve_order(index) {
  let order_id = $("#order-id-" + (index + 1)).text();

  $.ajax({
    type: "POST",
    url: "/api/approve_order",
    data: {
      order_id: order_id,
    },
    success: function (response) {
      console.log(response);
      if (response["result"] === "success") {
        window.location.reload();
      }
    },
  });
}

function decline_order(index) {
  let order_id = $("#order-id-" + (index + 1)).text();

  $.ajax({
    type: "POST",
    url: "/api/decline_order",
    data: {
      order_id: order_id,
    },
    success: function (response) {
      console.log(response);
      if (response["result"] === "success") {
        window.location.reload();
      }
    },
  });
}

function complete_order(index) {
  let order_id = $("#order-id-" + (index + 1)).text();

  $.ajax({
    type: "POST",
    url: "/api/complete_order",
    data: {
      order_id: order_id,
    },
    success: function (response) {
      console.log(response);
      if (response["result"] === "success") {
        window.location.reload();
      }
    },
  });
}

function proceed_review(index) {
  let order_id = $("#order-id-" + (index + 1)).text();
  $("#modal-review").modal("show");
  $("#order-id").val(order_id);
}

function add_rating() {
  let order_id = $("#order-id").val();
  let rating = $("#rating").val();

  $.ajax({
    type: "POST",
    url: "/api/add_rating",
    data: {
      order_id: order_id,
      rating: rating,
    },
    success: function (response) {
      console.log(response);
      if (response["result"] === "success") {
        window.location.reload();
      }
    },
  });
}
