// // $(document).ready(function() {
// //     $("#do_login").click(function() { 
// //        closeLoginInfo();
// //        $(this).parent().find('span').css("display","none");
// //        $(this).parent().find('span').removeClass("i-save");
// //        $(this).parent().find('span').removeClass("i-warning");
// //        $(this).parent().find('span').removeClass("i-close");

// //         var proceed = true;
// //         $("#login_form input").each(function(){

// //             if(!$.trim($(this).val())){
// //                 $(this).parent().find('span').addClass("i-warning");
// //             	$(this).parent().find('span').css("display","block");  
// //                 proceed = false;
// //             }
// //         });

// //         if(proceed) //everything looks good! proceed...
// //         {
// //             $(this).parent().find('span').addClass("i-save");
// //             $(this).parent().find('span').css("display","block");
// //         }
// //     });

// //     //reset previously results and hide all message on .keyup()
// //     $("#login_form input").keyup(function() { 
// //         $(this).parent().find('span').css("display","none");
// //     });

// //   openLoginInfo();
// //   setTimeout(closeLoginInfo, 1000);
// // });

// // function openLoginInfo() {
// //     $(document).ready(function(){ 
// //     	$('.b-form').css("opacity","0.01");
// //       $('.box-form').css("left","-37%");
// //       $('.box-info').css("right","-37%");
// //     });
// // }

// // function closeLoginInfo() {
// //     $(document).ready(function(){ 
// //     	$('.b-form').css("opacity","1");
// //     	$('.box-form').css("left","0px");
// //       $('.box-info').css("right","-5px"); 
// //     });
// // }

// // $(window).on('resize', function(){
// //       closeLoginInfo();
// // });
















// $(document).ready(function () {
//   // Initial effect (optional, can remove if not desired)
//   openLoginInfo();
//   setTimeout(closeLoginInfo, 1000);

//   // Handle login button click
//   $("#do_login").click(function (event) {
//     event.preventDefault(); // prevent default form submit behavior

//     closeLoginInfo();

//     const parent = $(this).parent();
//     parent.find("span").css("display", "none").removeClass("i-save i-warning i-close");

//     let proceed = true;

//     $("#login_form input[type='text'], #login_form input[type='password']").each(function () {
//       if (!$.trim($(this).val())) {
//         $(this).parent().find("span").addClass("i-warning").css("display", "block");
//         proceed = false;
//       }
//     });

//     if (proceed) {
//       parent.find("span").addClass("i-save").css("display", "block");
//     }
//   });

//   // Reset warnings on keyup
//   $("#login_form input").keyup(function () {
//     $(this).parent().find("span").css("display", "none");
//   });

//   // Handle window resize
//   $(window).on("resize", function () {
//     closeLoginInfo();
//   });
// });

// function openLoginInfo() {
//   $(".b-form").css("opacity", "0.01");
//   $(".box-form").css("left", "-57%");
//   $(".box-info").css("right", "-37%");
// }

// function closeLoginInfo() {
//   $(".b-form").css("opacity", "1");
//   $(".box-form").css("left", "0px");
//   $(".box-info").css("right", "-5px");
// }





// // $("#do_organize").click(function () {
// //   fetch("/api/sort", {
// //     method: "POST",
// //   })
// //     .then((response) => response.json())
// //     .then((data) => {
// //       alert(`Sorted ${data.files_sorted} files!`);
// //     })
// //     .catch((error) => {
// //       alert("Error: " + error.message);
// //     });
// // });













// // $("#do_organize").click(function (event) {
// //   event.preventDefault();

// //   fetch("/api/sort", {
// //     method: "POST",
// //   })
// //     .then((res) => res.json())
// //     .then((data) => {
// //       if (data.status === "success") {
// //         alert(`✅ Sorted ${data.files_sorted} files.`);
// //       } else {
// //         alert("⚠️ Error: " + data.message);
// //       }
// //     })
// //     .catch((err) => {
// //       alert("❌ Request failed: " + err.message);
// //     });
// // });












// $("#do_organize").click(function (event) {
//   event.preventDefault();

//   const source_folder = $("#source_folder").val().trim();
//   const categories = [];

//   $("#file_types input[type='checkbox']:checked").each(function () {
//     categories.push($(this).val());
//   });

//   fetch("/api/sort", {
//     method: "POST",
//     headers: {
//       "Content-Type": "application/json",
//     },
//     body: JSON.stringify({
//       source_folder: source_folder,
//       categories: categories,
//     }),
//   })
//     .then((res) => res.json())
//     .then((data) => {
//       if (data.status === "success") {
//         alert(`✅ Sorted ${data.files_sorted} files.`);
//       } else {
//         alert("⚠️ Error: " + data.message);
//       }
//     })
//     .catch((err) => {
//       alert("❌ Request failed: " + err.message);
//     });
// });


















// $(document).ready(function () {
//   // Initial animation
//   openLoginInfo();
//   setTimeout(closeLoginInfo, 3000);

//   // Handle login button click
//   $("#do_login").click(function (event) {
//     event.preventDefault();

//     closeLoginInfo();

//     const parent = $(this).parent();
//     parent.find("span").css("display", "none").removeClass("i-save i-warning i-close");

//     let proceed = true;

//     $("#login_form input[type='text'], #login_form input[type='password']").each(function () {
//       if (!$.trim($(this).val())) {
//         $(this).parent().find("span").addClass("i-warning").css("display", "block");
//         proceed = false;
//       }
//     });

//     if (proceed) {
//       parent.find("span").addClass("i-save").css("display", "block");
//     }
//   });

//   // Reset warnings on keyup
//   $("#login_form input").keyup(function () {
//     $(this).parent().find("span").css("display", "none");
//   });

//   // Handle window resize
//   $(window).on("resize", function () {
//     closeLoginInfo();
//   });

//   // Handle Organize button click
//   $("#do_organize").click(function (event) {
//     event.preventDefault();

//     const folder = $("#source_folder").val().trim();
//     if (!folder) {
//       alert("Please enter a folder path.");
//       return;
//     }

//     $("#log-output").val("Organizing files...\n");

//     fetch("/organize", {
//       method: "POST",
//       headers: {
//         "Content-Type": "application/json"
//       },
//       body: JSON.stringify({ folder: folder })
//     })
//       .then(response => response.json())
//       .then(data => {
//         $("#log-output").val(data.log);
//       })
//       .catch(error => {
//         $("#log-output").val("An error occurred:\n" + error);
//       });
//   });

//   $("#source_folder").click(async function () {
//     const folder = await window.pywebview.api.choose_folder();
//     if (folder) {
//       $(this).val(folder);
//     }
//   });

// });

// function openLoginInfo() {
//   $(".b-form").css("opacity", "0.01");
//   $(".box-form").css("left", "-57%");
//   $(".box-info").css("right", "-37%");
// }

// function closeLoginInfo() {
//   $(".b-form").css("opacity", "1");
//   $(".box-form").css("left", "0px");
//   $(".box-info").css("right", "-5px");
// }




// $(document).ready(function () {
//   openLoginInfo();
//   setTimeout(closeLoginInfo, 1000);

//   $("#do_organize").click(function (event) {
//     event.preventDefault();

//     const folder = $("#source_folder").val().trim();
//     const destination = $("#enable-destination").is(":checked") ? $("#destination-folder").val().trim() : '';
//     const keywords = $("#keywords").val().trim();
//     const includeSubfolders = $("#include-subfolders").is(":checked");
//     const dateSorting = $("#date-sorting").is(":checked");

//     let filters = [];
//     $(".file-types input[type='checkbox']").each(function () {
//       if ($(this).is(":checked")) {
//         filters.push($(this).parent().text().trim());
//       }
//     });

//     if (!folder) {
//       alert("Please select a folder.");
//       return;
//     }

//     $("#log-output").val("Organizing files...\n");

//     fetch("/organize", {
//       method: "POST",
//       headers: {
//         "Content-Type": "application/json"
//       },
//       body: JSON.stringify({
//         source_folder: folder,
//         destination_folder: destination,
//         keywords: keywords,
//         include_subfolders: includeSubfolders,
//         date_sorting: dateSorting,
//         filters: filters
//       })
//     })
//       .then(response => response.json())
//       .then(data => {
//         $("#log-output").val(data.message + "\n" + (data.log || ''));
//       })
//       .catch(error => {
//         $("#log-output").val("An error occurred:\n" + error);
//       });
//   });

//   $("#source_folder, #destination-folder").click(async function () {
//     const folder = await window.pywebview.api.choose_folder();
//     if (folder) {
//       $(this).val(folder);
//     }
//   });

//   // Drag-and-drop support
//   $("#source_folder").on("dragover", e => e.preventDefault());
//   $("#source_folder").on("drop", e => {
//     e.preventDefault();
//     const path = e.originalEvent.dataTransfer.files[0].path;
//     $("#source_folder").val(path);
//   });
// });
