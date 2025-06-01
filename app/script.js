$(document).ready(function () {
  // Initial login animation
  openLoginInfo();
  setTimeout(closeLoginInfo, 1000);

  // Login logic
  $("#do_login").click(function (event) {
    event.preventDefault();

    closeLoginInfo();
    const parent = $(this).parent();
    parent.find("span").css("display", "none").removeClass("i-save i-warning i-close");

    let proceed = true;
    $("#login_form input[type='text'], #login_form input[type='password']").each(function () {
      if (!$.trim($(this).val())) {
        $(this).parent().find("span").addClass("i-warning").css("display", "block");
        proceed = false;
      }
    });

    if (proceed) {
      parent.find("span").addClass("i-save").css("display", "block");
    }
  });

  // Reset warnings on keyup
  $("#login_form input").keyup(function () {
    $(this).parent().find("span").css("display", "none");
  });

  // Window resize closes login panel
  $(window).on("resize", function () {
    closeLoginInfo();
  });

  // Organize logic
  $("#do_organize").click(function (event) {
    event.preventDefault();

    const folder = $("#source_folder").val().trim();
    const destination = $("#enable-destination").is(":checked") ? $("#destination-folder").val().trim() : '';
    const keywords = $("#keywords").val().trim();
    const includeSubfolders = $("#include-subfolders").is(":checked");
    const dateSorting = $("#date-sorting").is(":checked");

    let filters = [];
    $(".file-types input[type='checkbox']").each(function () {
      if ($(this).is(":checked")) {
        filters.push($(this).parent().text().trim());
      }
    });

    if (!folder) {
      alert("Please select a folder.");
      return;
    }

    $("#log-output").val("Organizing files...\n");

    fetch("/organize", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        source_folder: folder,
        destination_folder: destination,
        keywords: keywords,
        include_subfolders: includeSubfolders,
        date_sorting: dateSorting,
        filters: filters
      })
    })
      .then(response => response.json())
      .then(data => {
        $("#log-output").val(data.message + "\n" + (data.log || ''));
      })
      .catch(error => {
        $("#log-output").val("An error occurred:\n" + error);
      });
  });


    // Undo organize logic
  $("#undo_organize").click(function (event) {
    event.preventDefault();

    $("#log-output").val("Reversing file organization...\n");

    fetch("/undo", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      }
    })
      .then(response => response.json())
      .then(data => {
        $("#log-output").val(data.message + "\n" + (data.log || ""));
      })
      .catch(error => {
        $("#log-output").val("An error occurred:\n" + error);
      });
  });


  // Folder picker
  $("#source_folder, #destination-folder").click(async function () {
    const folder = await window.pywebview.api.choose_folder();
    if (folder) {
      $(this).val(folder);
    }
  });

  // Enable/disable destination field
  $("#enable-destination").change(function () {
    const isChecked = $(this).is(":checked");
    $("#destination-folder").prop("disabled", !isChecked);
    if (!isChecked) {
      $("#destination-folder").val('');
    }
  });

  // Drag-and-drop support for source folder
  $("#source_folder")
    .on("dragover", function (e) {
      e.preventDefault();
      e.originalEvent.dataTransfer.dropEffect = 'copy';
    })
    .on("drop", function (e) {
      e.preventDefault();
      const files = e.originalEvent.dataTransfer.files;
      if (files.length > 0) {
        const folderPath = files[0].path;
        $(this).val(folderPath);
      }
    });

  // Filter checkbox logic: "All" toggles
  $(".file-types input[type='checkbox']").change(function () {
    const label = $(this).parent().text().trim().toLowerCase();

    if (label === "all") {
      if ($(this).is(":checked")) {
        // Uncheck all others
        $(".file-types input[type='checkbox']").not(this).prop("checked", false);
      }
    } else {
      // Uncheck "All" if any specific filter is checked
      $(".file-types input[type='checkbox']").each(function () {
        const l = $(this).parent().text().trim().toLowerCase();
        if (l === "all") {
          $(this).prop("checked", false);
        }
      });
    }
  });
});

// Login animation functions
function openLoginInfo() {
  $(".b-form").css("opacity", "0.01");
  $(".box-form").css("left", "-57%");
  $(".box-info").css("right", "-37%");
}

function closeLoginInfo() {
  $(".b-form").css("opacity", "1");
  $(".box-form").css("left", "0px");
  $(".box-info").css("right", "-5px");
}


