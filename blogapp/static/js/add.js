// ADD Categories

    // Function to get CSRF token from cookies
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    const csrftoken = getCookie('csrftoken');

    // Set up AJAX to include CSRF token
    $.ajaxSetup({
        headers: { 'X-CSRFToken': csrftoken }
    });

    $(document).ready(function () {

        // Preview the selected image
        $('#id_image').on('change', function (event) {
            const file = event.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function (e) {
                    $('#imagePreview').attr('src', e.target.result).show();
                };
                reader.readAsDataURL(file);
            } else {
                $('#imagePreview').hide();
            }
        });

        // Form validation and submission
        $('#blogCategoryForm').submit(function (event) {
            event.preventDefault(); // Prevent form submission for validation

            // Clear previous error messages
            $('#nameError').text('');
            $('#imageError').text('');

            const categoryName = $('#id_name').val().trim();
            const categoryImage = $('#id_image').val();
            let valid = true;

            // Validate Category Name
            if (!categoryName) {
                $('#nameError').text('Category name is required.');
                valid = false;
            } else if (!/^[A-Z][a-zA-Z]*$/.test(categoryName)) {
                $('#nameError').text('Category name must start with a capital letter and contain only letters.');
                valid = false;
            }

            // Validate Category Image
            if (!categoryImage) {
                $('#imageError').text('Category image is required.');
                valid = false;
            }

            // If valid, check if the category name exists on the server
            if (valid) {
                $.ajax({
                    url: checkCategoryUrl, // Use the evaluated URL
                    method: 'POST',
                    data: {
                        'name': categoryName,
                        'csrfmiddlewaretoken': csrftoken // Include CSRF token
                    },
                    success: function (response) {
                        if (response.exists) {
                            $('#nameError').text(`Category "${categoryName}" already exists.`);
                        } else {
                            // Submit the form if it does not exist
                            $.ajax({
                                url: "", // Leave this blank to post to the same URL
                                method: 'POST',
                                data: new FormData($('#blogCategoryForm')[0]), // Send form data
                                processData: false,
                                contentType: false,
                                success: function (data) {
                                    if (data.success) {
                                        alert('Category added successfully!'); // Show success alert
                                        window.location.href = data.redirect_url; // Redirect to category list
                                    } else {
                                        // Handle errors returned from the server
                                        for (const error in data.errors) {
                                            $('#nameError').text(data.errors[error]);
                                        }
                                    }
                                },
                                error: function () {
                                    alert('An error occurred while adding the category.');
                                }
                            });
                        }
                    },
                    error: function () {
                        alert('An error occurred while checking the category.');
                    }
                });
            }
        });
    });


    
//////////// Update Categories ////////////
$(document).ready(function () {
    // Preview the selected image
    $('#id_image').on('change', function (event) {
        const file = event.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function (e) {
                $('#imagePreview').attr('src', e.target.result).show();
            };
            reader.readAsDataURL(file);
        } else {
            $('#imagePreview').hide();
        }
    });

    // Handle form submission
    $('#blogCategoryUpdateForm').submit(function (event) {
        event.preventDefault(); // Prevent default form submission

        $('#nameError').text('');  // Clear previous error messages
        $('#imageError').text('');

        const categoryName = $('#id_name').val().trim();
        let valid = true;

        // Validate category name
        if (!categoryName) {
            $('#nameError').text('Category name is required.');
            valid = false;
        } else if (!/^[A-Z][a-zA-Z]*$/.test(categoryName)) {
            $('#nameError').text('Category name must start with a capital letter and contain only letters.');
            valid = false;
        }

        // If the input is valid, check if the category exists
        if (valid) {
            $.ajax({
                url: checkCategoryUrl, // URL to check if the category exists
                method: 'POST',
                data: {
                    'name': categoryName,
                    'csrfmiddlewaretoken': csrftoken // Include CSRF token
                },
                success: function (response) {
                    if (response.exists) {
                        $('#nameError').text(`Category "${categoryName}" already exists.`);
                    } else {
                        // If the category doesn't exist, submit the form via AJAX
                        const formData = new FormData($('#blogCategoryUpdateForm')[0]); // Ensure the correct form data is used
                        $.ajax({
                            url: ajaxUrl, // URL for updating the category
                            type: 'POST',
                            data: formData,
                            processData: false,
                            contentType: false,
                            success: function (data) {
                                // Show success alert when the form submission is successful
                                alert('Category updated successfully!');

                                // Redirect to the category list page using the redirect URL from the response
                                if (data.success) {
                                    window.location.href = data.redirect_url; // Ensure this URL is correct
                                }
                            },
                            error: function () {
                                alert('An error occurred while updating the category.');
                            }
                        });
                    }
                },
                error: function () {
                    $('#nameError').text('An error occurred while checking for existing categories.');
                }
            });
        }
    });
});
