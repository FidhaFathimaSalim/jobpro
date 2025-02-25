$(document).ready(function () {
    $('.container2').repeater({
        initEmpty: false,
        defaultValues: {
            'project': '',
            'project_description': '',
            'project_link': ''
        },
        show: function () {
            $(this).slideDown();
        },
        hide: function (deleteElement) {
            $(this).slideUp(deleteElement);
        },
        isFirstItemUndeletable: false,
        ready: function (setIndexes) {
            // This function is called after the repeater is initialized
        }
    });

    $(document).ready(function () {
        $('.container4').repeater({
            initEmpty: false,
            defaultValues: {
                'certificate': '',
                'certificate_description': '',
            },
            show: function () {
                $(this).slideDown();
            },
            hide: function (deleteElement) {
                $(this).slideUp(deleteElement);
            },
            isFirstItemUndeletable: false,
            ready: function (setIndexes) {
                // This function is called after the repeater is initialized
            }
        });

$(document).ready(function () {
        $('.container21').repeater({
            initEmpty: false,
            defaultValues: {
                'language': '',
            },
            show: function () {
                $(this).slideDown();
            },
            hide: function (deleteElement) {
                $(this).slideUp(deleteElement);
            },
            isFirstItemUndeletable: false,
            ready: function (setIndexes) {
                // This function is called after the repeater is initialized
            }
        });

    // Add click event for the delete button near the heading
    $('.repeater-remove-btn').on('click', function () {
        const repeaterItems = $('[data-repeater-item]');
        if (repeaterItems.length > 0) {
            repeaterItems.last().remove(); // Remove the last project entry
        }
    });
    });
    $('.repeater-remove-btn1').on('click', function () {
        const repeaterItems = $('[data-repeater-item]');
        if (repeaterItems.length > 0) {
            repeaterItems.last().remove(); // Remove the last project entry
        }
    });
    });
    $('.repeater-remove-btn2').on('click', function () {
        const repeaterItems = $('[data-repeater-item]');
        if (repeaterItems.length > 0) {
            repeaterItems.last().remove(); // Remove the last project entry
        }
    });
})
